#[derive(Debug, PartialEq, Eq)]
pub enum QuoteError {
    InvalidDiscount,
}

/// Returns a local quote in the input currency's minor units, rounding down.
/// This calculation does not authorize payment or perform external effects.
pub fn quote(subtotal_minor: u64, discount_bps: u16) -> Result<u64, QuoteError> {
    if discount_bps > 10_000 {
        return Err(QuoteError::InvalidDiscount);
    }
    let scaled = u128::from(subtotal_minor) * u128::from(10_000 - discount_bps);
    // A factor in [0, 10000] makes the rounded result no larger than the input.
    Ok((scaled / 10_000) as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn preserves_defined_rounding_and_bounds() {
        assert_eq!(quote(10_005, 500), Ok(9_504));
        assert_eq!(quote(0, 500), Ok(0));
        assert_eq!(quote(u64::MAX, 0), Ok(u64::MAX));
        assert_eq!(quote(u64::MAX, 10_000), Ok(0));
        assert_eq!(quote(100, 10_001), Err(QuoteError::InvalidDiscount));
        assert_eq!(quote(100, u16::MAX), Err(QuoteError::InvalidDiscount));
    }

    #[test]
    fn total_never_increases_as_discount_increases() {
        for subtotal in [0, 1, 100, 10_005, u64::MAX] {
            let mut previous = subtotal;
            for discount in 0..=10_000 {
                let current = quote(subtotal, discount).expect("valid discount");
                assert!(current <= previous);
                previous = current;
            }
        }
    }
}
