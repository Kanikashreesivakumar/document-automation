/** Converts a number to English words for the "Amount Chargeable in Words" field */
export function numberToWords(num: number): string {
  if (isNaN(num) || num === 0) return '';

  const ones = ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE',
    'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN',
    'SEVENTEEN', 'EIGHTEEN', 'NINETEEN'];
  const tens = ['', '', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY', 'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY'];

  function toWords(n: number): string {
    if (n === 0) return '';
    if (n < 20) return ones[n] + ' ';
    if (n < 100) return tens[Math.floor(n / 10)] + ' ' + (n % 10 !== 0 ? ones[n % 10] + ' ' : '');
    if (n < 1000) return ones[Math.floor(n / 100)] + ' HUNDRED ' + toWords(n % 100);
    if (n < 100000) return toWords(Math.floor(n / 1000)) + 'THOUSAND ' + toWords(n % 1000);
    if (n < 10000000) return toWords(Math.floor(n / 100000)) + 'LAKH ' + toWords(n % 100000);
    return toWords(Math.floor(n / 10000000)) + 'CRORE ' + toWords(n % 10000000);
  }

  const intPart = Math.floor(num);
  const decPart = Math.round((num - intPart) * 100);

  let result = 'US$: ' + toWords(intPart).trim();
  if (decPart > 0) {
    result += ' AND CENTS ' + toWords(decPart).trim();
  }
  return result.trim() + ' ONLY';
}
