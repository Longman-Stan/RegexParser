grammar rGex;
 
regex: regex '|' regex2 | regex2;
regex2: regex2 regex3 | regex3;
regex3: kleene | plus | qmark | repeat | regex4;
kleene: regex4 '*';
plus: regex4 '+';
qmark: regex4 '?';
repeat: single | regex4 '{' repeatAtom ',' repeatAtom '}';
single: regex4 '{' repeatAtom '}';
repeatAtom: number |;
regex4: paranthesis | anY | seT | continut;
anY: '.';
paranthesis: '(' regex ')';
seT: '[' setvals ']';
setvals: rangE setvals | continut setvals|;
continut: DIGIT | LALPHA | HALPHA;
rangE: DIGIT '-' DIGIT | LALPHA '-' LALPHA | HALPHA '-' HALPHA;
number: DIGIT number| DIGIT; 

DIGIT: [0-9];
LALPHA: [a-z];
HALPHA: [A-Z];
