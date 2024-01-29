/*------------------------------------------------------------------
 * REGLAS SINTACTICAS
 *------------------------------------------------------------------*/
grammar RiscV;
prog : finlinea* (bloquedatos|bloquecodigo)* EOF;



finlinea : NUEVALINEA| COMENTARIO;

// ***************************************
// ***** REGLAS DEL BLOQUE DE DATOS *****
// ***************************************
// No se va a poder elegir donde se almacenan los datos
bloquedatos : ZONADATOS finlinea lineadatos*;

lineadatos : ETIQUETA? {InfoCompil.Program.addTag($ETIQUETA, "variable");} declaracion? finlinea;

declaracion     : T_SPACE tamRes=NUMERO_INT
                | var_int=(T_WORD|T_HALF|T_BYTE)  vi+=NUMERO_INT (COMA vi+=NUMERO_INT)*   {InfoCompil.Tags.AddVariables($var_int, $vi);    }
                | var_fp=(T_FLOAT|T_DOUBLE)       vf+=NUMERO_FP  (COMA vf+=NUMERO_FP)*    {InfoCompil.Tags.AddVariables($var_fp, $vf);     }
                | var_string=(T_ASCII|T_ASCIIZ)   vs+=CADENA     (COMA vf+=CADENA)*       {InfoCompil.Tags.AddVariables($var_string, $vs); }
                ;




// ***************************************
// ***** REGLAS DEL BLOQUE DE CODIGO *****
// ***************************************
bloquecodigo    : ZONACODIGO  finlinea lineacodigo*;

lineacodigo     : ETIQUETA?                  {InfoCompil.Tags.Add($ETIQUETA, "code");}  instruccion? finlinea;

reg_int : REG_INT|REG_INT_NAME;
inm_int : NUMERO_INT;
parEtiq : IDENT;

instruccion: op = (SLL|SRL|SRA|ADD|SUB|XOR|OR|AND|SLT|SLTU|MUL|MULH|MULHSU|MULHU|DIV|DIVU|REM|REMU)
         r1=reg_int  COMA  r2=reg_int  COMA    r3=reg_int          { InfoCompil.Instruction.addInstI1($op,r1, r2, r3);}
     | op = (ADDI|ANDI|ORI|XORI|SLTI|SLTIU)      r1=reg_int  COMA  r2=reg_int   COMA    inm=inm_int            { InfoCompil.Instructions.addInstI2($op,r1,r2,inm);}// Tipo I:    Op rd, rs1, Inm12
     | op = (SLLI|SRLI|SRAI)                     r1=reg_int  COMA  r2=reg_int   COMA    inm=inm_int            { InfoCompil.Instructions.addInstI3($op,r1,r2,inm);}// Tipo I:    Op rd, rs1, Shamt5
     | op= (LB|LBU|LH|LHU|LW)                   r1=reg_int  COMA  inm=inm_int  LPAREN   rs=reg_int   RPAREN   { InfoCompil.Instructions.addInstI4($op,r1,inm,rs);}// Tipo I:    Op rd, Inm12(rs1)
     | op= (SB|SH|SW)                           r1=reg_int  COMA  inm=inm_int  LPAREN  rs=reg_int   RPAREN   { InfoCompil.Instructions.addInstS1($op,r1,inm,rs);}// Tipo S:    Op rs1,Inm12(rs2)
     | op= (LUI|AUIPC)                          r1=reg_int  COMA  inm=inm_int                                 { InfoCompil.Instructions.addInstU1($op,r1,inm);}// Tipo U:    Op rd, Inm20
     | op= (ECALL|EBREAK)                                                                                     { InfoCompil.Instructions.addInstI5($op);}// Tipo I:    Op
     | op= (BEQ|BNE|BLT|BLTU|BGE|BGEU)          r1=reg_int  COMA  r2=reg_int   COMA    inm=inm_int            { InfoCompil.Instructions.addInstB1($op,r1,r2,inm);}// Tipo B:    bxx rs1, rs2, inm13/Etiq
     | op= JAL                                  r1=reg_int  COMA  inm=inm_int                                 { InfoCompil.Instructions.addInstJ1($op,r1,inm);}// Tipo J:    jal rd, Inm21/Etiq
     | op= JALR                                 r1=reg_int  COMA  r2=reg_int   COMA    inm=inm_int            { InfoCompil.Instructions.addInstI6($op,r1,r2,inm);}// Tipo I:    jalr rd, rs1, Inm12/Etiq
     | op= JALR                                 r1=reg_int  COMA  inm=inm_int  LPAREN   rs=reg_int   RPAREN   { InfoCompil.Instructions.addInstI7($op,r1,inm,rs);};// Tipo I:    jalr rd, Inm12/Etiq(rs1)  // Otra forma de encontrarlo





// **************************
// ***** REGLAS LÉXICAS *****
// **************************

ZONADATOS             : '.data';
ZONACODIGO            : '.text';
ZONACONFIGURACION     : '.config';
T_EQV : '.eqv';

COMA         : ',';
LPAREN  : '(';
RPAREN  : ')';

PIPELINED   : 'pipelined';
FORWARDING  : 'forwarding' ;
DELAYED     : 'delayed';
SPLIT       : 'split';
UNALIGNED   : 'unaligned';
OVERWRITECODE: 'overwritecode';
FULLACCESS : 'fullaccess';

ON         : 'on';
OFF        : 'off';

EXI        : 'exi';
EXM        : 'exm';
EXD        : 'exd';
EXFP       : 'exfp';
EXFPM      : 'exfpm';
EXFPD      : 'exfpd';

MEMORY     : 'memory';

CACHE      : 'cache';
ICACHE     : 'icache';
DCACHE     : 'dcache';
SIZE       : 'size';
BLOCK      : 'block';
WAY        : 'way';
WRITE      : 'write';
CBWA       : 'cbwa';
WTNWA      : 'wtnwa';
REPLACE    : 'replace';
RANDOM     : 'random';
LRU        : 'lru';
FIFO       : 'fifo';
LFU        : 'lfu';
ADDDEV     : 'adddev';
BOARD      : 'board';
ARROWS     : 'arrows';
MATRIX     : 'matrix';
KEYBOARD   : 'keyboard';
SCREEN     : 'screen';

BITBUSY    : 'bitbusy';
BITNEWCHAR : 'bitnewchar';
LATENCY    : 'latency';
FILAS      : 'rows';
COLS       : 'columns';

IGUAL      : '=';
PATTERN    : 'pattern';


    // JUEGO DE INSTRUCCIONES BASE DE RV32I
LUI: 'lui';
AUIPC: 'auipc';
JAL: 'jal';
JALR: 'jalr';
BEQ: 'beq';
BNE: 'bne';
BLT: 'blt';
BGE: 'bge';
BLTU: 'bltu';
BGEU: 'bgeu';
LB: 'lb';
LH: 'lh';
LW: 'lw';
LBU: 'lbu';
LHU: 'lhu';
SB: 'sb';
SH: 'sh';
SW: 'sw';
ADDI: 'addi';
SLTI: 'slti';
SLTIU: 'sltiu';
XORI: 'xori';
ORI: 'ori';
ANDI: 'andi';
SLLI: 'slli';
SRLI: 'srli';
SRAI: 'srai';
ADD : 'add';
SUB: 'sub';
SLL: 'sll';
SLT: 'slt';
SLTU:'sltu';
XOR: 'xor';
SRL: 'srl';
SRA: 'sra';
OR: 'or';
AND: 'and';
//FENCE
//DENCE.I
ECALL: 'ecall';
EBREAK: 'ebreak';
//CSRRW
//CSRRS
//CSRRC
//CSRRWI
//CSRRSI
//CSRRCI


// ******** Instrucciones de la Extensión Estándar RV32M *********
MUL: 'mul';
MULH: 'mulh';
MULHSU: 'mulhsu';
MULHU: 'mulhu';
DIV: 'div';
DIVU: 'divu';
REM: 'rem';
REMU: 'remu';

// ****** PSEUDOINSTRUCCIONES RISCV ******
LA: 'la';
//FL
//FS
NOP : 'nop';
LI: 'li';
MV: 'mv';
NOT: 'not';
NEG: 'neg';
//NEGW
//SEXT
SEQZ: 'seqz';
SNEZ: 'snez';
SLTZ: 'sltz';
SGTZ: 'sgtz';
//FMVS
//FABSS
//FNEGS
//FMVD
//FABD
//FNEGD
BEQZ: 'beqz';
BNEZ: 'bnez';
BLEZ: 'blez';
BGEZ: 'bgez';
BLTZ: 'bltz';
BGTZ: 'bgtz';
BGT: 'bgt';
BLE: 'ble';
BGTU: 'bgtu';
BLEU: 'bleu';
J: 'j';
JR: 'jr';       //JUMPR --> Tipo R:   jr rs | jalr rs | jalr rs,rd  // Nota jalr podría llevar retorno en otro != de R31
RET: 'ret';
//CALL

// ********** INSTRUCCIONES MIPS A VERIFICAR SI EXISTEN O HAY EQUIVALENCIA EN RISCV
//NOR: 'nor'; ROR: 'ror'; ROL: 'rol'; ABS: 'abs' ; B: 'b';
//SEQ:'seq'; SGT:'sgt'; SGTU:'sgtu'; SGE:'sge'; SGEU:'sgeu'; SLE:'sle'; SLEU:'sleu'; SNE:'sne';
//BC1F:'bc1f'; BC1T:'bc1t'; BGEZAL:'bgezal'; BLTZAL:'bltzal'; CLO:'clo'; CLZ:'clz';
//LWL:'lwl'; LWR:'lwr'; SWL:'swl'; SWR:'swr';

// ********* ARITMÉTICAS FP DE MIPS ***************
//ADDS: 'add.s'; SUBS: 'sub.s'; MULS: 'mul.s'; DIVS: 'div.s';ABSS: 'abs.s';
//ADDD: 'add.d'; SUBD: 'sub.d'; MULD:'mul.d'; DIVD: 'div.d'; ABSD: 'abs.d';
// ************ LOAD/STORE FP DE MIPS *************
//LWC1: 'lwc1'; LDC1: 'ldc1'; SWC1: 'swc1'; SDC1: 'sdc1'; MFC1: 'mfc1'; MTC1: 'mtc1';
// ************ COMPARAR FP DE MIPS ***************
//CEQD:'c.eq.d'; CEQS:'c.eq.s'; CLED:'c.le.d'; CLES:'c.le.s'; CLTD:'c.lt.d'; CLTS:'c.lt.s';
// ************ CONVERSIONES FP y WORD DE MIPS ************
//CVTDS:'cvt.d.s'; CVTDW:'cvt.d.w'; CVTSD:'cvt.s.d'; /CVTSW:'cvt.s.w'; CVTWD:'cvt.w.d'; CVTWS:'cvt.w.s';
// ************ OTRAS DE FP EN MIPS*************
// MOVD: 'mov.d'; MOVS:'mov.s'; NEGD:'neg.d'; NEGS:'neg.s'; SQRTD:'sqrt.d'; SQRTS:'sqrt.s';
// TRUNCWD:'trunc.w.d'; TRUNCWS:'trunc.w.s'; ROUNDWD:'round.w.d'; ROUNDWS:'round.w.s'; FLOORWD:'floor.w.d'; FLOORWS:'floor.w.s'; CEILWD:'ceil.w.d'; CEILWS:'ceil.w.s';

T_WORD       : '.word';
T_HALF       : '.half';
T_BYTE       : '.byte';
T_FLOAT      : '.float';
T_DOUBLE     : '.double';
T_ASCII     : '.ascii';
T_ASCIIZ    : '.asciiz';

T_SPACE      : '.space';

CADENA       :'"' .*? '"';                  // Esto va antes que ESPACIOS, NUEVALINEA
COMENTARIO   : '#'.*? '\n'('\r'?'\n')*;    // Ya no se admiten comentarios mediante ( COMENTARIO : (';'|'#') .*? '\n'('\r'?'\n')*; )
ESPACIOS     : (' '|'\t')+ -> skip ;
NUEVALINEA   : ('\r'?'\n')+;
PATRONBITS   : '{' .*? '}';     //('.'|'?'|'0'|'1'|','|LETRA)+
REG_FP       : ('f10'|'f11'|'f12'|'f13'|'f14'|'f15'|'f16'|'f17'|'f18'|'f19'|'f20'|'f21'|'f22'|'f23'|'f24'|'f25'|'f26'|'f27'|'f28'|'f29'|'f30'|'f31'|'f0'|'f1'|'f2'|'f3'|'f4'|'f5'|'f6'|'f7'|'f8'|'f9');
REG_FP_NAME  : ('ft0'|'ft1'|'ft2'|'ft3'|'ft4'|'ft5'|'ft6'|'ft7'|'fs0'|'fs1'|'fa0'|'fa1'|'fa2'|'fa3'|'fa4'|'fa5'|'fa6'|'fa7'|'fs2'|'fs3'|'fs4'|'fs5'|'fs6'|'fs7'|'fs8'|'fs9'|'fs10'|'fs11'|'ft8'|'ft9'|'ft10'|'ft11');
REG_INT      : ('x10'|'x11'|'x12'|'x13'|'x14'|'x15'|'x16'|'x17'|'x18'|'x19'|'x20'|'x21'|'x22'|'x23'|'x24'|'x25'|'x26'|'x27'|'x28'|'x29'|'x30'|'x31'|'x0'|'x1'|'x2'|'x3'|'x4'|'x5'|'x6'|'x7'|'x8'|'x9');
REG_INT_NAME : ('zero'|'ra'|'sp'|'gp'|'tp'|'t0'|'t1'|'t2'|'s0'|'s1'|'a0'|'a1'|'a2'|'a3'|'a4'|'a5'|'a6'|'a7'|'s2'|'s3'|'s4'|'s5'|'s6'|'s7'|'s8'|'s9'|'s10'|'s11'|'t3'|'t4'|'t5'|'t6');
NUMERO_INT   : NUMERO_B10|NUMERO_HEX;
NUMERO_FP    : (('+'|'-') DIGITO)? DIGITO* '.' DIGITO+ ; //  1.123  .123  -1.123 pero no -.123
ETIQUETA     : IDENT ':';

IDENT        : (LETRA|'_'|'.') (LETRA|DIGITO|'_'|'.')*; // Este debe ir después de ETIQUETA pero antes de RESTO (y antes de los fragment). AÑADE '.' PARA LA AYUDA EMERGENTE EN EL EDITOR
CARACTERROR  : . ;   // Recoge el resto como un Token de Carácter error para trasladar los erróres léxicos a sintácticos (crea token de error)

fragment NUMERO_B10 :('+'|'-')? DIGITO+ ('K'|'k')?;
fragment NUMERO_HEX : ('+'|'-')?('0x')(DIGITO|LETRAHEX)+;
fragment DIGITO  : '0'..'9';
fragment LETRAHEX: 'a'..'f'|'A'..'F';
fragment LETRA   : 'a'..'z'|'A'..'Z';

