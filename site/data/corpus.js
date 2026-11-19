window.AUC = {
 "units": [
  {
   "id": "00AC",
   "char": "¬",
   "name": "NOT SIGN",
   "def": "Negation: 'not' — true exactly when p is false",
   "vis": "\\u00AC",
   "family": "logic"
  },
  {
   "id": "2227",
   "char": "∧",
   "name": "LOGICAL AND",
   "def": "Conjunction: 'and' — true exactly when both p and q are true",
   "vis": "\\u2227",
   "family": "logic"
  },
  {
   "id": "2228",
   "char": "∨",
   "name": "LOGICAL OR",
   "def": "Disjunction: 'or' (inclusive) — true when p or q or both are true",
   "vis": "\\u2228",
   "family": "logic"
  },
  {
   "id": "2192",
   "char": "→",
   "name": "RIGHTWARDS ARROW",
   "def": "Implication: 'if ... then ...' — false only when p is true and q is false",
   "vis": "\\u2192",
   "family": "logic"
  },
  {
   "id": "2194",
   "char": "↔",
   "name": "LEFT RIGHT ARROW",
   "def": "Biconditional: 'if and only if' — true exactly when p and q have the same truth value",
   "vis": "\\u2194",
   "family": "logic"
  },
  {
   "id": "2283",
   "char": "⊃",
   "name": "SUPERSET OF",
   "def": "Implication (alternative notation): 'if ... then ...', same connective as U+2192",
   "vis": "\\u2283",
   "family": "logic"
  },
  {
   "id": "2261",
   "char": "≡",
   "name": "IDENTICAL TO",
   "def": "Equivalence: 'is equivalent to' — p and q have the same truth value in every case",
   "vis": "\\u2261",
   "family": "logic"
  },
  {
   "id": "22A5",
   "char": "⊥",
   "name": "UP TACK",
   "def": "Falsum: the constant false proposition, always false; also marks a contradiction",
   "vis": "\\u22A5",
   "family": "logic"
  },
  {
   "id": "22A4",
   "char": "⊤",
   "name": "DOWN TACK",
   "def": "Verum: the constant true proposition, always true",
   "vis": "\\u22A4",
   "family": "logic"
  },
  {
   "id": "22A2",
   "char": "⊢",
   "name": "RIGHT TACK",
   "def": "Proves: p can be derived (proved) from the premises by the rules of the system",
   "vis": "\\u22A2",
   "family": "logic"
  },
  {
   "id": "22A8",
   "char": "⊨",
   "name": "TRUE",
   "def": "Entails: p is true in every interpretation in which all the premises are true",
   "vis": "\\u22A8",
   "family": "logic"
  },
  {
   "id": "2234",
   "char": "∴",
   "name": "THEREFORE",
   "def": "Therefore: marks the conclusion of an argument",
   "vis": "\\u2234",
   "family": "logic"
  },
  {
   "id": "2235",
   "char": "∵",
   "name": "BECAUSE",
   "def": "Because: marks a reason or premise for a claim",
   "vis": "\\u2235",
   "family": "logic"
  },
  {
   "id": "2295",
   "char": "⊕",
   "name": "CIRCLED PLUS",
   "def": "Exclusive or (circled-plus form): true exactly when exactly one of p, q is true",
   "vis": "\\u2295",
   "family": "logic"
  },
  {
   "id": "22BB",
   "char": "⊻",
   "name": "XOR",
   "def": "Exclusive or: true exactly when exactly one of p, q is true",
   "vis": "\\u22BB",
   "family": "logic"
  },
  {
   "id": "2191",
   "char": "↑",
   "name": "UPWARDS ARROW",
   "def": "Sheffer stroke (NAND): 'not (p and q)' — true except when both p and q are true",
   "vis": "\\u2191",
   "family": "logic"
  },
  {
   "id": "22AC",
   "char": "⊬",
   "name": "DOES NOT PROVE",
   "def": "Does not prove: p cannot be derived from the premises",
   "vis": "\\u22AC",
   "family": "logic"
  },
  {
   "id": "22AD",
   "char": "⊭",
   "name": "NOT TRUE",
   "def": "Does not entail: p is not a semantic consequence of the premises",
   "vis": "\\u22AD",
   "family": "logic"
  },
  {
   "id": "0020",
   "char": " ",
   "name": "SPACE",
   "def": "The ordinary word space. In an encoded stream it stays the literal byte 0x20.",
   "vis": "\\u0020",
   "family": "whitespace"
  },
  {
   "id": "000A",
   "char": "\n",
   "name": "LINE FEED",
   "def": "The new-line character. Literal in an encoded stream when newlines are preserved, which is the default; encoded otherwise.",
   "vis": "\\u000A",
   "family": "whitespace"
  },
  {
   "id": "000D",
   "char": "\r",
   "name": "CARRIAGE RETURN",
   "def": "The return key character. Always encoded, so a CRLF pair round-trips as the CR code followed by a literal line feed.",
   "vis": "\\u000D",
   "family": "whitespace"
  },
  {
   "id": "0021",
   "char": "!",
   "name": "EXCLAMATION MARK",
   "def": "Exclamation mark: the printable ASCII character at U+0021, encoded as \\u0021.",
   "vis": "\\u0021",
   "family": "ascii"
  },
  {
   "id": "0022",
   "char": "\"",
   "name": "QUOTATION MARK",
   "def": "Quotation mark: the printable ASCII character at U+0022, encoded as \\u0022.",
   "vis": "\\u0022",
   "family": "ascii"
  },
  {
   "id": "0023",
   "char": "#",
   "name": "NUMBER SIGN",
   "def": "Number sign: the printable ASCII character at U+0023, encoded as \\u0023.",
   "vis": "\\u0023",
   "family": "ascii"
  },
  {
   "id": "0024",
   "char": "$",
   "name": "DOLLAR SIGN",
   "def": "Dollar sign: the printable ASCII character at U+0024, encoded as \\u0024.",
   "vis": "\\u0024",
   "family": "ascii"
  },
  {
   "id": "0025",
   "char": "%",
   "name": "PERCENT SIGN",
   "def": "Percent sign: the printable ASCII character at U+0025, encoded as \\u0025.",
   "vis": "\\u0025",
   "family": "ascii"
  },
  {
   "id": "0026",
   "char": "&",
   "name": "AMPERSAND",
   "def": "Ampersand: the printable ASCII character at U+0026, encoded as \\u0026.",
   "vis": "\\u0026",
   "family": "ascii"
  },
  {
   "id": "0027",
   "char": "'",
   "name": "APOSTROPHE",
   "def": "Apostrophe: the printable ASCII character at U+0027, encoded as \\u0027.",
   "vis": "\\u0027",
   "family": "ascii"
  },
  {
   "id": "0028",
   "char": "(",
   "name": "LEFT PARENTHESIS",
   "def": "Left parenthesis: the printable ASCII character at U+0028, encoded as \\u0028.",
   "vis": "\\u0028",
   "family": "ascii"
  },
  {
   "id": "0029",
   "char": ")",
   "name": "RIGHT PARENTHESIS",
   "def": "Right parenthesis: the printable ASCII character at U+0029, encoded as \\u0029.",
   "vis": "\\u0029",
   "family": "ascii"
  },
  {
   "id": "002A",
   "char": "*",
   "name": "ASTERISK",
   "def": "Asterisk: the printable ASCII character at U+002A, encoded as \\u002A.",
   "vis": "\\u002A",
   "family": "ascii"
  },
  {
   "id": "002B",
   "char": "+",
   "name": "PLUS SIGN",
   "def": "Plus sign: the printable ASCII character at U+002B, encoded as \\u002B.",
   "vis": "\\u002B",
   "family": "ascii"
  },
  {
   "id": "002C",
   "char": ",",
   "name": "COMMA",
   "def": "Comma: the printable ASCII character at U+002C, encoded as \\u002C.",
   "vis": "\\u002C",
   "family": "ascii"
  },
  {
   "id": "002D",
   "char": "-",
   "name": "HYPHEN-MINUS",
   "def": "Hyphen-minus: the printable ASCII character at U+002D, encoded as \\u002D.",
   "vis": "\\u002D",
   "family": "ascii"
  },
  {
   "id": "002E",
   "char": ".",
   "name": "FULL STOP",
   "def": "Full stop: the printable ASCII character at U+002E, encoded as \\u002E.",
   "vis": "\\u002E",
   "family": "ascii"
  },
  {
   "id": "002F",
   "char": "/",
   "name": "SOLIDUS",
   "def": "Solidus: the printable ASCII character at U+002F, encoded as \\u002F.",
   "vis": "\\u002F",
   "family": "ascii"
  },
  {
   "id": "0030",
   "char": "0",
   "name": "DIGIT ZERO",
   "def": "Digit zero: the printable ASCII character at U+0030, encoded as \\u0030.",
   "vis": "\\u0030",
   "family": "ascii"
  },
  {
   "id": "0031",
   "char": "1",
   "name": "DIGIT ONE",
   "def": "Digit one: the printable ASCII character at U+0031, encoded as \\u0031.",
   "vis": "\\u0031",
   "family": "ascii"
  },
  {
   "id": "0032",
   "char": "2",
   "name": "DIGIT TWO",
   "def": "Digit two: the printable ASCII character at U+0032, encoded as \\u0032.",
   "vis": "\\u0032",
   "family": "ascii"
  },
  {
   "id": "0033",
   "char": "3",
   "name": "DIGIT THREE",
   "def": "Digit three: the printable ASCII character at U+0033, encoded as \\u0033.",
   "vis": "\\u0033",
   "family": "ascii"
  },
  {
   "id": "0034",
   "char": "4",
   "name": "DIGIT FOUR",
   "def": "Digit four: the printable ASCII character at U+0034, encoded as \\u0034.",
   "vis": "\\u0034",
   "family": "ascii"
  },
  {
   "id": "0035",
   "char": "5",
   "name": "DIGIT FIVE",
   "def": "Digit five: the printable ASCII character at U+0035, encoded as \\u0035.",
   "vis": "\\u0035",
   "family": "ascii"
  },
  {
   "id": "0036",
   "char": "6",
   "name": "DIGIT SIX",
   "def": "Digit six: the printable ASCII character at U+0036, encoded as \\u0036.",
   "vis": "\\u0036",
   "family": "ascii"
  },
  {
   "id": "0037",
   "char": "7",
   "name": "DIGIT SEVEN",
   "def": "Digit seven: the printable ASCII character at U+0037, encoded as \\u0037.",
   "vis": "\\u0037",
   "family": "ascii"
  },
  {
   "id": "0038",
   "char": "8",
   "name": "DIGIT EIGHT",
   "def": "Digit eight: the printable ASCII character at U+0038, encoded as \\u0038.",
   "vis": "\\u0038",
   "family": "ascii"
  },
  {
   "id": "0039",
   "char": "9",
   "name": "DIGIT NINE",
   "def": "Digit nine: the printable ASCII character at U+0039, encoded as \\u0039.",
   "vis": "\\u0039",
   "family": "ascii"
  },
  {
   "id": "003A",
   "char": ":",
   "name": "COLON",
   "def": "Colon: the printable ASCII character at U+003A, encoded as \\u003A.",
   "vis": "\\u003A",
   "family": "ascii"
  },
  {
   "id": "003B",
   "char": ";",
   "name": "SEMICOLON",
   "def": "Semicolon: the printable ASCII character at U+003B, encoded as \\u003B.",
   "vis": "\\u003B",
   "family": "ascii"
  },
  {
   "id": "003C",
   "char": "<",
   "name": "LESS-THAN SIGN",
   "def": "Less-than sign: the printable ASCII character at U+003C, encoded as \\u003C.",
   "vis": "\\u003C",
   "family": "ascii"
  },
  {
   "id": "003D",
   "char": "=",
   "name": "EQUALS SIGN",
   "def": "Equals sign: the printable ASCII character at U+003D, encoded as \\u003D.",
   "vis": "\\u003D",
   "family": "ascii"
  },
  {
   "id": "003E",
   "char": ">",
   "name": "GREATER-THAN SIGN",
   "def": "Greater-than sign: the printable ASCII character at U+003E, encoded as \\u003E.",
   "vis": "\\u003E",
   "family": "ascii"
  },
  {
   "id": "003F",
   "char": "?",
   "name": "QUESTION MARK",
   "def": "Question mark: the printable ASCII character at U+003F, encoded as \\u003F.",
   "vis": "\\u003F",
   "family": "ascii"
  },
  {
   "id": "0040",
   "char": "@",
   "name": "COMMERCIAL AT",
   "def": "Commercial at: the printable ASCII character at U+0040, encoded as \\u0040.",
   "vis": "\\u0040",
   "family": "ascii"
  },
  {
   "id": "0041",
   "char": "A",
   "name": "LATIN CAPITAL LETTER A",
   "def": "Latin capital letter a: the printable ASCII character at U+0041, encoded as \\u0041.",
   "vis": "\\u0041",
   "family": "ascii"
  },
  {
   "id": "0042",
   "char": "B",
   "name": "LATIN CAPITAL LETTER B",
   "def": "Latin capital letter b: the printable ASCII character at U+0042, encoded as \\u0042.",
   "vis": "\\u0042",
   "family": "ascii"
  },
  {
   "id": "0043",
   "char": "C",
   "name": "LATIN CAPITAL LETTER C",
   "def": "Latin capital letter c: the printable ASCII character at U+0043, encoded as \\u0043.",
   "vis": "\\u0043",
   "family": "ascii"
  },
  {
   "id": "0044",
   "char": "D",
   "name": "LATIN CAPITAL LETTER D",
   "def": "Latin capital letter d: the printable ASCII character at U+0044, encoded as \\u0044.",
   "vis": "\\u0044",
   "family": "ascii"
  },
  {
   "id": "0045",
   "char": "E",
   "name": "LATIN CAPITAL LETTER E",
   "def": "Latin capital letter e: the printable ASCII character at U+0045, encoded as \\u0045.",
   "vis": "\\u0045",
   "family": "ascii"
  },
  {
   "id": "0046",
   "char": "F",
   "name": "LATIN CAPITAL LETTER F",
   "def": "Latin capital letter f: the printable ASCII character at U+0046, encoded as \\u0046.",
   "vis": "\\u0046",
   "family": "ascii"
  },
  {
   "id": "0047",
   "char": "G",
   "name": "LATIN CAPITAL LETTER G",
   "def": "Latin capital letter g: the printable ASCII character at U+0047, encoded as \\u0047.",
   "vis": "\\u0047",
   "family": "ascii"
  },
  {
   "id": "0048",
   "char": "H",
   "name": "LATIN CAPITAL LETTER H",
   "def": "Latin capital letter h: the printable ASCII character at U+0048, encoded as \\u0048.",
   "vis": "\\u0048",
   "family": "ascii"
  },
  {
   "id": "0049",
   "char": "I",
   "name": "LATIN CAPITAL LETTER I",
   "def": "Latin capital letter i: the printable ASCII character at U+0049, encoded as \\u0049.",
   "vis": "\\u0049",
   "family": "ascii"
  },
  {
   "id": "004A",
   "char": "J",
   "name": "LATIN CAPITAL LETTER J",
   "def": "Latin capital letter j: the printable ASCII character at U+004A, encoded as \\u004A.",
   "vis": "\\u004A",
   "family": "ascii"
  },
  {
   "id": "004B",
   "char": "K",
   "name": "LATIN CAPITAL LETTER K",
   "def": "Latin capital letter k: the printable ASCII character at U+004B, encoded as \\u004B.",
   "vis": "\\u004B",
   "family": "ascii"
  },
  {
   "id": "004C",
   "char": "L",
   "name": "LATIN CAPITAL LETTER L",
   "def": "Latin capital letter l: the printable ASCII character at U+004C, encoded as \\u004C.",
   "vis": "\\u004C",
   "family": "ascii"
  },
  {
   "id": "004D",
   "char": "M",
   "name": "LATIN CAPITAL LETTER M",
   "def": "Latin capital letter m: the printable ASCII character at U+004D, encoded as \\u004D.",
   "vis": "\\u004D",
   "family": "ascii"
  },
  {
   "id": "004E",
   "char": "N",
   "name": "LATIN CAPITAL LETTER N",
   "def": "Latin capital letter n: the printable ASCII character at U+004E, encoded as \\u004E.",
   "vis": "\\u004E",
   "family": "ascii"
  },
  {
   "id": "004F",
   "char": "O",
   "name": "LATIN CAPITAL LETTER O",
   "def": "Latin capital letter o: the printable ASCII character at U+004F, encoded as \\u004F.",
   "vis": "\\u004F",
   "family": "ascii"
  },
  {
   "id": "0050",
   "char": "P",
   "name": "LATIN CAPITAL LETTER P",
   "def": "Latin capital letter p: the printable ASCII character at U+0050, encoded as \\u0050.",
   "vis": "\\u0050",
   "family": "ascii"
  },
  {
   "id": "0051",
   "char": "Q",
   "name": "LATIN CAPITAL LETTER Q",
   "def": "Latin capital letter q: the printable ASCII character at U+0051, encoded as \\u0051.",
   "vis": "\\u0051",
   "family": "ascii"
  },
  {
   "id": "0052",
   "char": "R",
   "name": "LATIN CAPITAL LETTER R",
   "def": "Latin capital letter r: the printable ASCII character at U+0052, encoded as \\u0052.",
   "vis": "\\u0052",
   "family": "ascii"
  },
  {
   "id": "0053",
   "char": "S",
   "name": "LATIN CAPITAL LETTER S",
   "def": "Latin capital letter s: the printable ASCII character at U+0053, encoded as \\u0053.",
   "vis": "\\u0053",
   "family": "ascii"
  },
  {
   "id": "0054",
   "char": "T",
   "name": "LATIN CAPITAL LETTER T",
   "def": "Latin capital letter t: the printable ASCII character at U+0054, encoded as \\u0054.",
   "vis": "\\u0054",
   "family": "ascii"
  },
  {
   "id": "0055",
   "char": "U",
   "name": "LATIN CAPITAL LETTER U",
   "def": "Latin capital letter u: the printable ASCII character at U+0055, encoded as \\u0055.",
   "vis": "\\u0055",
   "family": "ascii"
  },
  {
   "id": "0056",
   "char": "V",
   "name": "LATIN CAPITAL LETTER V",
   "def": "Latin capital letter v: the printable ASCII character at U+0056, encoded as \\u0056.",
   "vis": "\\u0056",
   "family": "ascii"
  },
  {
   "id": "0057",
   "char": "W",
   "name": "LATIN CAPITAL LETTER W",
   "def": "Latin capital letter w: the printable ASCII character at U+0057, encoded as \\u0057.",
   "vis": "\\u0057",
   "family": "ascii"
  },
  {
   "id": "0058",
   "char": "X",
   "name": "LATIN CAPITAL LETTER X",
   "def": "Latin capital letter x: the printable ASCII character at U+0058, encoded as \\u0058.",
   "vis": "\\u0058",
   "family": "ascii"
  },
  {
   "id": "0059",
   "char": "Y",
   "name": "LATIN CAPITAL LETTER Y",
   "def": "Latin capital letter y: the printable ASCII character at U+0059, encoded as \\u0059.",
   "vis": "\\u0059",
   "family": "ascii"
  },
  {
   "id": "005A",
   "char": "Z",
   "name": "LATIN CAPITAL LETTER Z",
   "def": "Latin capital letter z: the printable ASCII character at U+005A, encoded as \\u005A.",
   "vis": "\\u005A",
   "family": "ascii"
  },
  {
   "id": "005B",
   "char": "[",
   "name": "LEFT SQUARE BRACKET",
   "def": "Left square bracket: the printable ASCII character at U+005B, encoded as \\u005B.",
   "vis": "\\u005B",
   "family": "ascii"
  },
  {
   "id": "005C",
   "char": "\\",
   "name": "REVERSE SOLIDUS",
   "def": "Reverse solidus: the printable ASCII character at U+005C, encoded as \\u005C.",
   "vis": "\\u005C",
   "family": "ascii"
  },
  {
   "id": "005D",
   "char": "]",
   "name": "RIGHT SQUARE BRACKET",
   "def": "Right square bracket: the printable ASCII character at U+005D, encoded as \\u005D.",
   "vis": "\\u005D",
   "family": "ascii"
  },
  {
   "id": "005E",
   "char": "^",
   "name": "CIRCUMFLEX ACCENT",
   "def": "Circumflex accent: the printable ASCII character at U+005E, encoded as \\u005E.",
   "vis": "\\u005E",
   "family": "ascii"
  },
  {
   "id": "005F",
   "char": "_",
   "name": "LOW LINE",
   "def": "Low line: the printable ASCII character at U+005F, encoded as \\u005F.",
   "vis": "\\u005F",
   "family": "ascii"
  },
  {
   "id": "0060",
   "char": "`",
   "name": "GRAVE ACCENT",
   "def": "Grave accent: the printable ASCII character at U+0060, encoded as \\u0060.",
   "vis": "\\u0060",
   "family": "ascii"
  },
  {
   "id": "0061",
   "char": "a",
   "name": "LATIN SMALL LETTER A",
   "def": "Latin small letter a: the printable ASCII character at U+0061, encoded as \\u0061.",
   "vis": "\\u0061",
   "family": "ascii"
  },
  {
   "id": "0062",
   "char": "b",
   "name": "LATIN SMALL LETTER B",
   "def": "Latin small letter b: the printable ASCII character at U+0062, encoded as \\u0062.",
   "vis": "\\u0062",
   "family": "ascii"
  },
  {
   "id": "0063",
   "char": "c",
   "name": "LATIN SMALL LETTER C",
   "def": "Latin small letter c: the printable ASCII character at U+0063, encoded as \\u0063.",
   "vis": "\\u0063",
   "family": "ascii"
  },
  {
   "id": "0064",
   "char": "d",
   "name": "LATIN SMALL LETTER D",
   "def": "Latin small letter d: the printable ASCII character at U+0064, encoded as \\u0064.",
   "vis": "\\u0064",
   "family": "ascii"
  },
  {
   "id": "0065",
   "char": "e",
   "name": "LATIN SMALL LETTER E",
   "def": "Latin small letter e: the printable ASCII character at U+0065, encoded as \\u0065.",
   "vis": "\\u0065",
   "family": "ascii"
  },
  {
   "id": "0066",
   "char": "f",
   "name": "LATIN SMALL LETTER F",
   "def": "Latin small letter f: the printable ASCII character at U+0066, encoded as \\u0066.",
   "vis": "\\u0066",
   "family": "ascii"
  },
  {
   "id": "0067",
   "char": "g",
   "name": "LATIN SMALL LETTER G",
   "def": "Latin small letter g: the printable ASCII character at U+0067, encoded as \\u0067.",
   "vis": "\\u0067",
   "family": "ascii"
  },
  {
   "id": "0068",
   "char": "h",
   "name": "LATIN SMALL LETTER H",
   "def": "Latin small letter h: the printable ASCII character at U+0068, encoded as \\u0068.",
   "vis": "\\u0068",
   "family": "ascii"
  },
  {
   "id": "0069",
   "char": "i",
   "name": "LATIN SMALL LETTER I",
   "def": "Latin small letter i: the printable ASCII character at U+0069, encoded as \\u0069.",
   "vis": "\\u0069",
   "family": "ascii"
  },
  {
   "id": "006A",
   "char": "j",
   "name": "LATIN SMALL LETTER J",
   "def": "Latin small letter j: the printable ASCII character at U+006A, encoded as \\u006A.",
   "vis": "\\u006A",
   "family": "ascii"
  },
  {
   "id": "006B",
   "char": "k",
   "name": "LATIN SMALL LETTER K",
   "def": "Latin small letter k: the printable ASCII character at U+006B, encoded as \\u006B.",
   "vis": "\\u006B",
   "family": "ascii"
  },
  {
   "id": "006C",
   "char": "l",
   "name": "LATIN SMALL LETTER L",
   "def": "Latin small letter l: the printable ASCII character at U+006C, encoded as \\u006C.",
   "vis": "\\u006C",
   "family": "ascii"
  },
  {
   "id": "006D",
   "char": "m",
   "name": "LATIN SMALL LETTER M",
   "def": "Latin small letter m: the printable ASCII character at U+006D, encoded as \\u006D.",
   "vis": "\\u006D",
   "family": "ascii"
  },
  {
   "id": "006E",
   "char": "n",
   "name": "LATIN SMALL LETTER N",
   "def": "Latin small letter n: the printable ASCII character at U+006E, encoded as \\u006E.",
   "vis": "\\u006E",
   "family": "ascii"
  },
  {
   "id": "006F",
   "char": "o",
   "name": "LATIN SMALL LETTER O",
   "def": "Latin small letter o: the printable ASCII character at U+006F, encoded as \\u006F.",
   "vis": "\\u006F",
   "family": "ascii"
  },
  {
   "id": "0070",
   "char": "p",
   "name": "LATIN SMALL LETTER P",
   "def": "Latin small letter p: the printable ASCII character at U+0070, encoded as \\u0070.",
   "vis": "\\u0070",
   "family": "ascii"
  },
  {
   "id": "0071",
   "char": "q",
   "name": "LATIN SMALL LETTER Q",
   "def": "Latin small letter q: the printable ASCII character at U+0071, encoded as \\u0071.",
   "vis": "\\u0071",
   "family": "ascii"
  },
  {
   "id": "0072",
   "char": "r",
   "name": "LATIN SMALL LETTER R",
   "def": "Latin small letter r: the printable ASCII character at U+0072, encoded as \\u0072.",
   "vis": "\\u0072",
   "family": "ascii"
  },
  {
   "id": "0073",
   "char": "s",
   "name": "LATIN SMALL LETTER S",
   "def": "Latin small letter s: the printable ASCII character at U+0073, encoded as \\u0073.",
   "vis": "\\u0073",
   "family": "ascii"
  },
  {
   "id": "0074",
   "char": "t",
   "name": "LATIN SMALL LETTER T",
   "def": "Latin small letter t: the printable ASCII character at U+0074, encoded as \\u0074.",
   "vis": "\\u0074",
   "family": "ascii"
  },
  {
   "id": "0075",
   "char": "u",
   "name": "LATIN SMALL LETTER U",
   "def": "Latin small letter u: the printable ASCII character at U+0075, encoded as \\u0075.",
   "vis": "\\u0075",
   "family": "ascii"
  },
  {
   "id": "0076",
   "char": "v",
   "name": "LATIN SMALL LETTER V",
   "def": "Latin small letter v: the printable ASCII character at U+0076, encoded as \\u0076.",
   "vis": "\\u0076",
   "family": "ascii"
  },
  {
   "id": "0077",
   "char": "w",
   "name": "LATIN SMALL LETTER W",
   "def": "Latin small letter w: the printable ASCII character at U+0077, encoded as \\u0077.",
   "vis": "\\u0077",
   "family": "ascii"
  },
  {
   "id": "0078",
   "char": "x",
   "name": "LATIN SMALL LETTER X",
   "def": "Latin small letter x: the printable ASCII character at U+0078, encoded as \\u0078.",
   "vis": "\\u0078",
   "family": "ascii"
  },
  {
   "id": "0079",
   "char": "y",
   "name": "LATIN SMALL LETTER Y",
   "def": "Latin small letter y: the printable ASCII character at U+0079, encoded as \\u0079.",
   "vis": "\\u0079",
   "family": "ascii"
  },
  {
   "id": "007A",
   "char": "z",
   "name": "LATIN SMALL LETTER Z",
   "def": "Latin small letter z: the printable ASCII character at U+007A, encoded as \\u007A.",
   "vis": "\\u007A",
   "family": "ascii"
  },
  {
   "id": "007B",
   "char": "{",
   "name": "LEFT CURLY BRACKET",
   "def": "Left curly bracket: the printable ASCII character at U+007B, encoded as \\u007B.",
   "vis": "\\u007B",
   "family": "ascii"
  },
  {
   "id": "007C",
   "char": "|",
   "name": "VERTICAL LINE",
   "def": "Vertical line: the printable ASCII character at U+007C, encoded as \\u007C.",
   "vis": "\\u007C",
   "family": "ascii"
  },
  {
   "id": "007D",
   "char": "}",
   "name": "RIGHT CURLY BRACKET",
   "def": "Right curly bracket: the printable ASCII character at U+007D, encoded as \\u007D.",
   "vis": "\\u007D",
   "family": "ascii"
  },
  {
   "id": "007E",
   "char": "~",
   "name": "TILDE",
   "def": "Tilde: the printable ASCII character at U+007E, encoded as \\u007E.",
   "vis": "\\u007E",
   "family": "ascii"
  }
 ],
 "rules": [
  {
   "id": "R1",
   "name": "NOT-APPLY",
   "op": "¬",
   "arity": 1,
   "template": "It is not the case that {0}",
   "trigger": [
    "negation",
    "not",
    "false",
    "case"
   ],
   "glue": null,
   "affix": "^it is not the case that (.*?)\\.?$",
   "also": []
  },
  {
   "id": "R2",
   "name": "AND-JOIN",
   "op": "∧",
   "arity": 2,
   "template": "{0}, and {1}",
   "trigger": [
    "conjunction",
    "and",
    "both",
    "true"
   ],
   "glue": ",\\s+and\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R3",
   "name": "OR-JOIN",
   "op": "∨",
   "arity": 2,
   "template": "{0}, or {1}",
   "trigger": [
    "disjunction",
    "or",
    "inclusive",
    "both"
   ],
   "glue": ",\\s+or\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R4",
   "name": "IF-JOIN",
   "op": "→",
   "arity": 2,
   "template": "If {0}, then {1}",
   "trigger": [
    "implication",
    "if",
    "then",
    "false"
   ],
   "glue": "^if (.*?), then (.*)$",
   "affix": null,
   "also": []
  },
  {
   "id": "R5",
   "name": "IFF-JOIN",
   "op": "↔",
   "arity": 2,
   "template": "{0} if and only if {1}",
   "trigger": [
    "biconditional",
    "if",
    "only",
    "same",
    "value"
   ],
   "glue": "\\s+if and only if\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R6",
   "name": "IMPLIES-JOIN",
   "op": "⊃",
   "arity": 2,
   "template": "{0} implies {1}",
   "trigger": [
    "implication",
    "implies",
    "notation",
    "then"
   ],
   "glue": "\\s+implies\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R7",
   "name": "EQUIV-JOIN",
   "op": "≡",
   "arity": 2,
   "template": "{0} is equivalent to {1}",
   "trigger": [
    "equivalence",
    "equivalent",
    "value",
    "every"
   ],
   "glue": "\\s+is equivalent to\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R8",
   "name": "XOR-JOIN",
   "op": "⊕",
   "arity": 2,
   "template": "Exactly one of {0} and {1} is true",
   "trigger": [
    "exclusive",
    "exactly",
    "one",
    "true"
   ],
   "glue": "^exactly one of (.*?) and (.*?) is true$",
   "affix": null,
   "also": [
    "⊻"
   ]
  },
  {
   "id": "R9",
   "name": "NAND-JOIN",
   "op": "↑",
   "arity": 2,
   "template": "Not both {0} and {1}",
   "trigger": [
    "sheffer",
    "stroke",
    "nand",
    "both"
   ],
   "glue": "^not both (.*?) and (.*)$",
   "affix": null,
   "also": []
  },
  {
   "id": "R10",
   "name": "THEREFORE",
   "op": "∴",
   "arity": 2,
   "template": "{0}, therefore {1}",
   "trigger": [
    "therefore",
    "conclusion",
    "argument"
   ],
   "glue": ",\\s+therefore\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R11",
   "name": "BECAUSE",
   "op": "∵",
   "arity": 2,
   "template": "{0}, because {1}",
   "trigger": [
    "because",
    "reason",
    "premise",
    "claim"
   ],
   "glue": ",\\s+because\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R12",
   "name": "PROVES",
   "op": "⊢",
   "arity": 2,
   "template": "{0} proves {1}",
   "trigger": [
    "proves",
    "derived",
    "premises",
    "rules"
   ],
   "glue": "\\s+proves\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R13",
   "name": "ENTAILS",
   "op": "⊨",
   "arity": 2,
   "template": "{0} entails {1}",
   "trigger": [
    "entails",
    "semantic",
    "consequence",
    "interpretation"
   ],
   "glue": "\\s+entails\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R14",
   "name": "NOT-PROVES",
   "op": "⊬",
   "arity": 2,
   "template": "{0} does not prove {1}",
   "trigger": [
    "proves",
    "cannot",
    "derived",
    "negation"
   ],
   "glue": "\\s+does not prove\\s+",
   "affix": null,
   "also": []
  },
  {
   "id": "R15",
   "name": "NOT-ENTAILS",
   "op": "⊭",
   "arity": 2,
   "template": "{0} does not entail {1}",
   "trigger": [
    "entails",
    "consequence",
    "semantic",
    "negation"
   ],
   "glue": "\\s+does not entail\\s+",
   "affix": null,
   "also": []
  }
 ],
 "combos": [
  {
   "rule": "R1",
   "a": "00AC",
   "b": "2227",
   "expr": "¬ ∧",
   "definition": "It is not the case that «Conjunction: 'and' — true exactly when both p and q are true»"
  },
  {
   "rule": "R1",
   "a": "00AC",
   "b": "2228",
   "expr": "¬ ∨",
   "definition": "It is not the case that «Disjunction: 'or' (inclusive) — true when p or q or both are true»"
  },
  {
   "rule": "R1",
   "a": "00AC",
   "b": "2192",
   "expr": "¬ →",
   "definition": "It is not the case that «Implication: 'if ... then ...' — false only when p is true and q is false»"
  },
  {
   "rule": "R1",
   "a": "00AC",
   "b": "2194",
   "expr": "¬ ↔",
   "definition": "It is not the case that «Biconditional: 'if and only if' — true exactly when p and q have the same truth value»"
  },
  {
   "rule": "R2",
   "a": "2227",
   "b": "00AC",
   "expr": "∧ ¬",
   "definition": "p, and «Negation: 'not' — true exactly when p is false»"
  },
  {
   "rule": "R2",
   "a": "2227",
   "b": "2228",
   "expr": "∧ ∨",
   "definition": "p, and «Disjunction: 'or' (inclusive) — true when p or q or both are true»"
  },
  {
   "rule": "R2",
   "a": "2227",
   "b": "2192",
   "expr": "∧ →",
   "definition": "p, and «Implication: 'if ... then ...' — false only when p is true and q is false»"
  },
  {
   "rule": "R2",
   "a": "2227",
   "b": "2194",
   "expr": "∧ ↔",
   "definition": "p, and «Biconditional: 'if and only if' — true exactly when p and q have the same truth value»"
  },
  {
   "rule": "R3",
   "a": "2228",
   "b": "00AC",
   "expr": "∨ ¬",
   "definition": "p, or «Negation: 'not' — true exactly when p is false»"
  },
  {
   "rule": "R3",
   "a": "2228",
   "b": "2227",
   "expr": "∨ ∧",
   "definition": "p, or «Conjunction: 'and' — true exactly when both p and q are true»"
  },
  {
   "rule": "R3",
   "a": "2228",
   "b": "2192",
   "expr": "∨ →",
   "definition": "p, or «Implication: 'if ... then ...' — false only when p is true and q is false»"
  },
  {
   "rule": "R3",
   "a": "2228",
   "b": "2194",
   "expr": "∨ ↔",
   "definition": "p, or «Biconditional: 'if and only if' — true exactly when p and q have the same truth value»"
  },
  {
   "rule": "R4",
   "a": "2192",
   "b": "00AC",
   "expr": "→ ¬",
   "definition": "If p, then «Negation: 'not' — true exactly when p is false»"
  },
  {
   "rule": "R4",
   "a": "2192",
   "b": "2227",
   "expr": "→ ∧",
   "definition": "If p, then «Conjunction: 'and' — true exactly when both p and q are true»"
  },
  {
   "rule": "R4",
   "a": "2192",
   "b": "2228",
   "expr": "→ ∨",
   "definition": "If p, then «Disjunction: 'or' (inclusive) — true when p or q or both are true»"
  },
  {
   "rule": "R4",
   "a": "2192",
   "b": "2194",
   "expr": "→ ↔",
   "definition": "If p, then «Biconditional: 'if and only if' — true exactly when p and q have the same truth value»"
  },
  {
   "rule": "R5",
   "a": "2194",
   "b": "00AC",
   "expr": "↔ ¬",
   "definition": "p if and only if «Negation: 'not' — true exactly when p is false»"
  },
  {
   "rule": "R5",
   "a": "2194",
   "b": "2227",
   "expr": "↔ ∧",
   "definition": "p if and only if «Conjunction: 'and' — true exactly when both p and q are true»"
  },
  {
   "rule": "R5",
   "a": "2194",
   "b": "2228",
   "expr": "↔ ∨",
   "definition": "p if and only if «Disjunction: 'or' (inclusive) — true when p or q or both are true»"
  },
  {
   "rule": "R5",
   "a": "2194",
   "b": "2192",
   "expr": "↔ →",
   "definition": "p if and only if «Implication: 'if ... then ...' — false only when p is true and q is false»"
  },
  {
   "rule": "R6",
   "a": "2283",
   "b": "2261",
   "expr": "⊃ ≡",
   "definition": "p implies «Equivalence: 'is equivalent to' — p and q have the same truth value in every case»"
  },
  {
   "rule": "R6",
   "a": "2283",
   "b": "22A5",
   "expr": "⊃ ⊥",
   "definition": "p implies «Falsum: the constant false proposition, always false; also marks a contradiction»"
  },
  {
   "rule": "R6",
   "a": "2283",
   "b": "22A4",
   "expr": "⊃ ⊤",
   "definition": "p implies «Verum: the constant true proposition, always true»"
  },
  {
   "rule": "R7",
   "a": "2261",
   "b": "2283",
   "expr": "≡ ⊃",
   "definition": "p is equivalent to «Implication (alternative notation): 'if ... then ...', same connective as U+2192»"
  },
  {
   "rule": "R7",
   "a": "2261",
   "b": "22A5",
   "expr": "≡ ⊥",
   "definition": "p is equivalent to «Falsum: the constant false proposition, always false; also marks a contradiction»"
  },
  {
   "rule": "R7",
   "a": "2261",
   "b": "22A4",
   "expr": "≡ ⊤",
   "definition": "p is equivalent to «Verum: the constant true proposition, always true»"
  },
  {
   "rule": "R12",
   "a": "22A2",
   "b": "22A8",
   "expr": "⊢ ⊨",
   "definition": "p proves «Entails: p is true in every interpretation in which all the premises are true»"
  },
  {
   "rule": "R12",
   "a": "22A2",
   "b": "22AC",
   "expr": "⊢ ⊬",
   "definition": "p proves «Does not prove: p cannot be derived from the premises»"
  },
  {
   "rule": "R12",
   "a": "22A2",
   "b": "22AD",
   "expr": "⊢ ⊭",
   "definition": "p proves «Does not entail: p is not a semantic consequence of the premises»"
  },
  {
   "rule": "R13",
   "a": "22A8",
   "b": "22A2",
   "expr": "⊨ ⊢",
   "definition": "p entails «Proves: p can be derived (proved) from the premises by the rules of the system»"
  },
  {
   "rule": "R13",
   "a": "22A8",
   "b": "22AC",
   "expr": "⊨ ⊬",
   "definition": "p entails «Does not prove: p cannot be derived from the premises»"
  },
  {
   "rule": "R13",
   "a": "22A8",
   "b": "22AD",
   "expr": "⊨ ⊭",
   "definition": "p entails «Does not entail: p is not a semantic consequence of the premises»"
  },
  {
   "rule": "R14",
   "a": "22AC",
   "b": "22A2",
   "expr": "⊬ ⊢",
   "definition": "p does not prove «Proves: p can be derived (proved) from the premises by the rules of the system»"
  },
  {
   "rule": "R14",
   "a": "22AC",
   "b": "22A8",
   "expr": "⊬ ⊨",
   "definition": "p does not prove «Entails: p is true in every interpretation in which all the premises are true»"
  },
  {
   "rule": "R14",
   "a": "22AC",
   "b": "22AD",
   "expr": "⊬ ⊭",
   "definition": "p does not prove «Does not entail: p is not a semantic consequence of the premises»"
  },
  {
   "rule": "R15",
   "a": "22AD",
   "b": "22A2",
   "expr": "⊭ ⊢",
   "definition": "p does not entail «Proves: p can be derived (proved) from the premises by the rules of the system»"
  },
  {
   "rule": "R15",
   "a": "22AD",
   "b": "22A8",
   "expr": "⊭ ⊨",
   "definition": "p does not entail «Entails: p is true in every interpretation in which all the premises are true»"
  },
  {
   "rule": "R15",
   "a": "22AD",
   "b": "22AC",
   "expr": "⊭ ⊬",
   "definition": "p does not entail «Does not prove: p cannot be derived from the premises»"
  },
  {
   "rule": "R10",
   "a": "2234",
   "b": "2235",
   "expr": "∴ ∵",
   "definition": "p, therefore «Because: marks a reason or premise for a claim»"
  },
  {
   "rule": "R10",
   "a": "2234",
   "b": "2295",
   "expr": "∴ ⊕",
   "definition": "p, therefore «Exclusive or (circled-plus form): true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R10",
   "a": "2234",
   "b": "22BB",
   "expr": "∴ ⊻",
   "definition": "p, therefore «Exclusive or: true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R10",
   "a": "2234",
   "b": "2191",
   "expr": "∴ ↑",
   "definition": "p, therefore «Sheffer stroke (NAND): 'not (p and q)' — true except when both p and q are true»"
  },
  {
   "rule": "R11",
   "a": "2235",
   "b": "2234",
   "expr": "∵ ∴",
   "definition": "p, because «Therefore: marks the conclusion of an argument»"
  },
  {
   "rule": "R11",
   "a": "2235",
   "b": "2295",
   "expr": "∵ ⊕",
   "definition": "p, because «Exclusive or (circled-plus form): true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R11",
   "a": "2235",
   "b": "22BB",
   "expr": "∵ ⊻",
   "definition": "p, because «Exclusive or: true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R11",
   "a": "2235",
   "b": "2191",
   "expr": "∵ ↑",
   "definition": "p, because «Sheffer stroke (NAND): 'not (p and q)' — true except when both p and q are true»"
  },
  {
   "rule": "R8",
   "a": "2295",
   "b": "2234",
   "expr": "⊕ ∴",
   "definition": "Exactly one of p and «Therefore: marks the conclusion of an argument» is true"
  },
  {
   "rule": "R8",
   "a": "2295",
   "b": "2235",
   "expr": "⊕ ∵",
   "definition": "Exactly one of p and «Because: marks a reason or premise for a claim» is true"
  },
  {
   "rule": "R8",
   "a": "2295",
   "b": "22BB",
   "expr": "⊕ ⊻",
   "definition": "Exactly one of p and «Exclusive or: true exactly when exactly one of p, q is true» is true"
  },
  {
   "rule": "R8",
   "a": "2295",
   "b": "2191",
   "expr": "⊕ ↑",
   "definition": "Exactly one of p and «Sheffer stroke (NAND): 'not (p and q)' — true except when both p and q are true» is true"
  },
  {
   "rule": "R8",
   "a": "22BB",
   "b": "2234",
   "expr": "⊻ ∴",
   "definition": "Exactly one of p and «Therefore: marks the conclusion of an argument» is true"
  },
  {
   "rule": "R8",
   "a": "22BB",
   "b": "2235",
   "expr": "⊻ ∵",
   "definition": "Exactly one of p and «Because: marks a reason or premise for a claim» is true"
  },
  {
   "rule": "R8",
   "a": "22BB",
   "b": "2295",
   "expr": "⊻ ⊕",
   "definition": "Exactly one of p and «Exclusive or (circled-plus form): true exactly when exactly one of p, q is true» is true"
  },
  {
   "rule": "R8",
   "a": "22BB",
   "b": "2191",
   "expr": "⊻ ↑",
   "definition": "Exactly one of p and «Sheffer stroke (NAND): 'not (p and q)' — true except when both p and q are true» is true"
  },
  {
   "rule": "R9",
   "a": "2191",
   "b": "2234",
   "expr": "↑ ∴",
   "definition": "Not both p and «Therefore: marks the conclusion of an argument»"
  },
  {
   "rule": "R9",
   "a": "2191",
   "b": "2235",
   "expr": "↑ ∵",
   "definition": "Not both p and «Because: marks a reason or premise for a claim»"
  },
  {
   "rule": "R9",
   "a": "2191",
   "b": "2295",
   "expr": "↑ ⊕",
   "definition": "Not both p and «Exclusive or (circled-plus form): true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R9",
   "a": "2191",
   "b": "22BB",
   "expr": "↑ ⊻",
   "definition": "Not both p and «Exclusive or: true exactly when exactly one of p, q is true»"
  },
  {
   "rule": "R0",
   "a": "0020",
   "b": "000A",
   "expr": "  \n",
   "definition": "«The ordinary word space. In an encoded stream it stays the literal byte 0x20.» then «The new-line character. Literal in an encoded stream when newlines are preserved, which is the default; encoded otherwise.»"
  },
  {
   "rule": "R0",
   "a": "0020",
   "b": "000D",
   "expr": "  \r",
   "definition": "«The ordinary word space. In an encoded stream it stays the literal byte 0x20.» then «The return key character. Always encoded, so a CRLF pair round-trips as the CR code followed by a literal line feed.»"
  },
  {
   "rule": "R0",
   "a": "000A",
   "b": "000D",
   "expr": "\n \r",
   "definition": "«The new-line character. Literal in an encoded stream when newlines are preserved, which is the default; encoded otherwise.» then «The return key character. Always encoded, so a CRLF pair round-trips as the CR code followed by a literal line feed.»"
  }
 ],
 "pages": [
  {
   "id": "index.html",
   "href": "index.html",
   "short": "Master page"
  },
  {
   "id": "units/set-01-connectives.html",
   "href": "units/set-01-connectives.html",
   "short": "Connectives"
  },
  {
   "id": "units/set-02-constants.html",
   "href": "units/set-02-constants.html",
   "short": "Equivalence"
  },
  {
   "id": "units/set-03-proof.html",
   "href": "units/set-03-proof.html",
   "short": "Proof"
  },
  {
   "id": "units/set-04-argument.html",
   "href": "units/set-04-argument.html",
   "short": "Argument"
  },
  {
   "id": "units/set-05-whitespace.html",
   "href": "units/set-05-whitespace.html",
   "short": "Whitespace"
  },
  {
   "id": "units/set-06-punctuation.html",
   "href": "units/set-06-punctuation.html",
   "short": "ASCII punctuation"
  },
  {
   "id": "units/set-07-digits.html",
   "href": "units/set-07-digits.html",
   "short": "ASCII digits"
  },
  {
   "id": "units/set-08-uppercase.html",
   "href": "units/set-08-uppercase.html",
   "short": "ASCII capitals"
  },
  {
   "id": "units/set-09-lowercase.html",
   "href": "units/set-09-lowercase.html",
   "short": "ASCII small letters"
  },
  {
   "id": "combos/comb-01-connectives.html",
   "href": "combos/comb-01-connectives.html",
   "short": "Combinations: Connectives"
  },
  {
   "id": "combos/comb-02-constants.html",
   "href": "combos/comb-02-constants.html",
   "short": "Combinations: Equivalence"
  },
  {
   "id": "combos/comb-03-proof.html",
   "href": "combos/comb-03-proof.html",
   "short": "Combinations: Proof"
  },
  {
   "id": "combos/comb-04-argument.html",
   "href": "combos/comb-04-argument.html",
   "short": "Combinations: Argument"
  },
  {
   "id": "combos/comb-05-whitespace.html",
   "href": "combos/comb-05-whitespace.html",
   "short": "Combinations: Whitespace"
  },
  {
   "id": "learner.html",
   "href": "learner.html",
   "short": "The learner"
  }
 ]
};
