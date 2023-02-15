use std::{
    fs::{self, File},
    path::{Path, PathBuf}, vec, io::Write,
};

use indicatif::ProgressBar;

fn get_bit_sequence(p: &Path) -> Result<Vec<bool>, std::io::Error> {
    let bytes = fs::read(p)?;

    let mut bits: Vec<bool> = Vec::with_capacity(bytes.len() * 8);

    for b in &bytes {
        bits.push(bit_at(&(*b as usize), 0)?);
        bits.push(bit_at(&(*b as usize), 1)?);
        bits.push(bit_at(&(*b as usize), 2)?);
        bits.push(bit_at(&(*b as usize), 3)?);
        bits.push(bit_at(&(*b as usize), 4)?);
        bits.push(bit_at(&(*b as usize), 5)?);
        bits.push(bit_at(&(*b as usize), 6)?);
        bits.push(bit_at(&(*b as usize), 7)?);
    }

    return Ok(bits);
}

// For our purposes endian-ness doesn't matter
fn bit_at(i: &usize, n: usize) -> Result<bool, std::io::Error> {
    if n > 64 {
        Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Bit at index n is out of range",
        ))
    } else {
        Ok(i & (1 << n) != 0)
    }
}

fn block_entropy(data: &Vec<bool>, block_length: usize) -> f64 {
    let mut entropy: f64 = 0.0;

    let data_length = data.len() - block_length;

    let mut pattern: Vec<bool> = Vec::with_capacity(block_length as usize);
    for _ in 0..block_length {
        pattern.push(false);
    }

    let bar = ProgressBar::new(2usize.pow(block_length as u32) as u64);
    bar.println("Counting block occurences");
    let mut occurences;
    let mut p: f64;
    for i in 0..2usize.pow(block_length as u32) {
        occurences = 0;
        bar.inc(1);
        for j in 0..block_length {
            pattern[j] = bit_at(&i, j).unwrap();
        }

        for j in 0..data_length {
            if pattern.as_slice() == &data[j..j+block_length] {
                occurences += 1;
            }
        }

        if occurences != 0 {
            p = (occurences as f64) / (data_length as f64);

            entropy += p * (1.0f64 / p).log2();
        }
    }
    bar.finish();

    entropy
}

fn main() {
    let path = PathBuf::from("../dest_imgs/baboon.jpeg");
    let data = get_bit_sequence(&path).unwrap();

    let block_lengths: Vec<usize> = (1..=16).collect();
    let mut entropies_per_symbol = Vec::new();
    for m in &block_lengths {
        entropies_per_symbol.push(block_entropy(&data, *m) / (*m as f64));
    }

    let mut file = File::create("dump.txt").unwrap();
    file.write(format!("{:?}\n", entropies_per_symbol).as_bytes()).unwrap();

    println!("{:?}", data.len());
}

#[cfg(test)] mod tests {
    use super::*;

    #[test]
    fn test_bit_at() {
        assert!(bit_at(&3, 0).unwrap());
        assert!(bit_at(&3, 1).unwrap());

        assert!(!bit_at(&4, 0).unwrap());
        assert!(!bit_at(&4, 1).unwrap());
        assert!(bit_at(&4, 2).unwrap());
    }

    #[test]
    fn test_bit_at_with_u8() {
        let x = 3u8;
        assert!(bit_at(&(x as usize),0).unwrap());
        assert!(bit_at(&(x as usize),1).unwrap());

        let y = 4u8;
        assert!(!bit_at(&(y as usize),0).unwrap());
        assert!(!bit_at(&(y as usize),1).unwrap());
        assert!(bit_at(&(y as usize),2).unwrap());
    }
}
