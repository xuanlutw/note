function try_reg(reg, str) {
    console.log(reg.exec(str));
}

// Escape char
    reg1 = /\$\(\)\*\+\.\?\[\\\^\{\|/

// Control char
    reg2 = /\a\e\f\n\r\t\v/

// ASCII
    reg3 = /\x70/
    // console.log(reg3.exec("app"));

// One of many
    reg4 = /c[ae]l[ae]nd[ae]r/
    // range
    reg5 = /[a-fA-F0-9]/
    // not
    reg6 = /[^a-fA-F0-9]/
    // shorthand
        // \d = [0-9]
        // \D = [^0-9]
        // \s = [ \r\n\t\v] i.e. white space
        // \S = [^ \r\n\t\v]
        // \w = [a-zA-Z0-9_]
        // \W = [^a-zA-Z0-9_]
    reg7 = /\d\D\s\S\w\W/
        //try_reg(reg7, "1v 1_ ");
    // case
    reg8 = /www/i
        //try_reg(reg8, "WwW");

// Wildcard char
    // not include \n
    reg9 = /./
        //try_reg(reg9, "W");
        //try_reg(reg9, "\n");
    // include
    reg10 = /[\s\S]/
        //try_reg(reg10, "W");
        //try_reg(reg10, "\n");

// Location
    // start
    reg11 = /^hi/
        //try_reg(reg11, "hi");
        //try_reg(reg11, "ihi");
    // end
    reg12 = /hi$/
        //try_reg(reg12, "hi");
        //try_reg(reg12, "hii");
    // multiline
    reg13 = /^hi/m
        //try_reg(reg13, "12\nhi");
    
// Word boundary
    reg14 = /\bcat\b/
    reg15 = /\Bcat\B/
    reg16 = /\Bcat|cat\B/
        //try_reg(reg14, "cat category staccato");
        //try_reg(reg15, "cat category staccato");
        //try_reg(reg16, "cat category staccato");

// Unicode
    reg17 = /\u1221/
    // ... it is massive QQ

// Branch
    reg18 = /Taiwan|China/
        //try_reg(reg18, "Taiwan");
        //try_reg(reg18, "China");

// Group
    // capturing group
    reg19 = /\b(Taiwan|China)\b/
    // not capturing group
    reg20 = /\b(?:Taiwan|China)\b/
    // ECMA2018 support named group...
    // reg20-1 = /\b(?<country>Taiwan|China)\b/
    
// Backreference
    // \1 = first capture
    // \2 = second capture
    reg21 = /\b\d\d(\d\d)-\1-\1\b/
        //try_reg(reg21, "2008-08-08");
        //try_reg(reg21, "2018-08-08");
    // ECMA2018 support named group...
    // reg21-1 = /\b(?<country>Taiwan|China)\b\k<country>/

// (Greeay) Repeat
    // quantifier {n} or {n,m}, repeat before
    // {0,} = *
    // {1,} = +
    // {0,1} = ?
    // 100 digit number
    reg22 = /\b\d{100}\b/
    // 32bit hex might postfix h
    reg23 = /\b[a-f\d]{1,8}h?\b/
    // float number
    reg24 = /\d*\.\d+(e\d+)?\b/
        //try_reg(reg24, ".71828e49");

// (Lazy) Repeat
    // .* do as mush as it can, then engineer backtrace to fit remain part
    // it may be problem
    // <p>text1<\p><p>text2<\p>
    // lazy quantifier
    // *? +? ?? {n,m}?
    // do as less as it can
    reg25 = /<p>[\s\S]*<p>/
    reg26 = /<p>[\s\S]*?<p>/
        //try_reg(reg25, "<p>text1<\p><p>text2<\p>");
        //try_reg(reg26, "<p>text1<\p><p>text2<\p>");
    
// Possessive quantifiers
// Atomic group 
    // not include in js

// Look around
    // check but not output
    // lookahead (?=regexp)
    reg27 = /\w+(?=<\/b>)/
        //try_reg(reg27, "My <b>cat</b> is furry.")
    // negative lookahead (?!regexp)
    reg28 = /\w+(?!<\/b>)/
        //try_reg(reg28, "My <b>cat</b> is furry.")
    // ECMA2018 support lookbehind...
    // alternative way
    reg29 = /(<b>)(\w+)(?=<\/b>)/
        //try_reg(reg29, "My <b>cat</b> is furry.")
    //reg29-1 = /(?<=<b>\w+(?=<\/b>)/
   
// Condition
    // js not support????
    // (?(1)then|else)
    //reg29-1 = /\b(?:(?:(one)|(two)|(three))(?:,|\b)){3,}/(?(1)|(?!))(?(2)|(?!))(?(3)|(?!))/
        //try_reg(reg30, "one,two,three")

// Find all
    reg30 = /.*/g
        try_reg(reg30, "My <b>cat</b> is furry.")
