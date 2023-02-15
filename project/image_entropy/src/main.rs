use std::{
    fs,
    path::{Path, PathBuf},
};

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

fn block_entropy(data: &Vec<bool>, m: u32) -> f64 {
    let mut entropy: f64 = 0.0;

    for i in [0..2usize.pow(m) - 1] {}

    entropy
}

fn main() {
    let path = PathBuf::from("../dest_imgs/baboon.png");
    let data = get_bit_sequence(&path).unwrap();

    println!("{:?}", data.len());
}

#[cfg(test)]
mod tests {
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
