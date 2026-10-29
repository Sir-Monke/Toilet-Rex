#!/usr/bin/env python3
"""T-rex on the throne, as animated text art. Python 3.8+, no dependencies.

Run:  python3 trex_art.py      Quit: Ctrl-C
Needs a truecolour terminal (Windows Terminal, iTerm2, kitty, GNOME Terminal...).
"""
import base64, math, os, platform, random, shutil, sys, time, zlib

FPS = 20
# Terminal.app before macOS 26 only does 256 colours; everything else gets truecolour
TRUECOLOUR = (os.environ.get("COLORTERM") in ("truecolor", "24bit")
              or os.environ.get("TERM_PROGRAM") != "Apple_Terminal"
              or int((platform.mac_ver()[0] or "0").split(".")[0]) >= 26)
RAMP = " .:-=+*#%@"
SW, SH = 200, 100  # baked image, pre-squashed 2:1 for character cells
DATA = """
c-nNmA)NE96Ezwc8Hq$9kw_#Gi9{liNF)-8L`FtNMn*<PMpjm?yl2Sn^MAj4zx({=?VIhk-8MO#IWx>m*|aRv#O8_5(}G*R2)PKg
NVn+7Oky@OpM{H(i$y7+t&&;_DQ5aN!Pqk6SyD0Mq|zKF#3IEa@KS8y%S;Cx2NUksS{Ng>5ynexxv?Bi#LF_VFfnsAE5De+Tvw{P
CB!8Z*c>xifE6;IhtV-}p|<jKZ$D@I?&a?B?%`_jS@T)rQRA9J@iu!GjP=%e=dHFe<W_qO$vLm_ZiMB+Flo8=i}tg0v-C_y?u&>O
pMTMTDJPV(K8Bd_MEozMlyk;^J|-WtO-+QhxH!8oyENOxoKxB6O&^y!Z+YJAy7_g>+Ll~+TSe=vR$lN&0*j6(FO!pAb0ZcfrBliZ
PR5yGOfj6#nNA~Tj4jJD<9aQ0@);L&4-VM)kKv@V3HJ!WtWiqg+Hvo#)m$#P(C-tch0!fzGsEw3O>vQMj6cC=E@q_}U?9e=G@R>Y
QS&@(lJlY#rWd@eS>XaNcq0DdjHlx@00^Lh-pC>)!{wHe!*G>xt%Y8+V>Sw(qz%G)!VIAf5D++E^jt=OQHtaI`A8O`HdYcc30nBD
02RGe;7}QDa7l3)gEC&>VNx@^d1dIG8!zxzTx7Ayuo{u{62lzp9Qzc@6zb$(1E`9~UFODP!P8<XpXdA@{j=q}C){2w9N7a`-@V>F
?<Mr)Tk<71YYqL=R%>TWur6s6q{4de%0_A8qWm;KHLHMiwb;D4%v_c(Tc3kZDdrq=N(B~E_6cyxIu;qQ{L&oK<n!dp<m!wUjHVoV
J;i=4_eY$!*mu6|eBW^(*Dh<}DYD>}6oj`t1(m!CP8eJc!JU#pORof=1zh1CEx5!AeIYcUg<Bj6x+K69uANr2uoo_8tXX3KZ61?$
LHZy|R>>_AkXxpia5du<aK(MpsbIxuAqY{x6)qpJN^lhf(V5SSTwt@DX95*|oL`s`z!b3tkSU$PEunguwdW>q<GFVHg+1T~2Ac<c
0naZf&C|3DBW7FhGK5g#H$Ze5;2(yifr}Rdtqma1C}9*=lBt1MZKN_nf~*{XN{DqyglcUurdXA=DasVBvS%?Zu`aQJmqaSAuVGz%
ZK2k_?e}#b>$a9!OF8%L+55AWXRAQh&xzyw*~)jTU@hS4?qx5rr_fT!F$U*}y0lly0aTzaZ4*o=&xD=1onXRE(oZVPCNIR-Mfu`F
iLnA#AtWENaS@!$U@qYSOTfGBSQR3ru;sMdvWfK&`zek~T#w!kS(=C$S6RfwV`K>jxZI8zJp)wEGH+S%U@e{;i<Sqy6fYaVW<-$O
;RLb;+-j6mlAuI4bjxUIgNzu~vXFy#LeQn?b+xTZ@L|HraB~jJ(R8+4aX6-#a76@#tF~yvv;i!cpkKkW09qiQiHQlTo`bjy2fjg2
!U^dFZt?yYK<^DVY8s@+w3q=uU{dk4%FuY~(ndzaIQWc%(*A(741lpe<ABy{c;q}D_V2gT?~kBstyu^nXH~1pMdl)ElZB4KX~GAV
D*mYU-Kr9JN-ULOi4c_tQE-1eL;&fyuAlGo^PHb^e~#_m*1eSCT=k$Jf35wyug}_k&i#8Ggt4tYTLHT0cB@;7HG*ph7QK{~ORp`*
;$8ASJD;@;09Z^7W_@AOP2BuJE6ye@4&Js%S4=3{XVACy$;7H-mA=4NGAx1AmelbPbaw49&sW`_<$RX)WOd_k*YJuaz|$_$G6(>$
G?x?T+5_5_`v5$O))W|QU1bKA-INn6iRB36@RGnofv>bYdubILnB+Lg$%_(YNgz6jRcy3yR(L0^;ogcc;OZUmVK6MnxmoZi&<M=T
%RtvW*aNh{i3|y55#9&xBQO`a!-sBOXD`62Iq}y@6gA2gP0O=nFBE_qqBTW6+gIT`j~kDx0N(>zcnHK3{|}b_Y&`q_a{mh|QfOER
R?o?^-ejvBw>9%t1z8i&5+o`%*>_cU<M9bgTvC~FQDUR31J{=7gv$_eKk;w-d9DxWY3qY_QjH;4>)^(;fhPn1MeABhdo4fL@j2Gd
xjpcSdjo^*#kXjq!}^wZh7Sc)6G<Iq@1d-sH9qIo+jbtubzbYbuiNQUmEbWK0UmB6l+~;WT_iMZT1=d@n~Ym5(G-lN6g(hNR^idt
BitYT{jkro94F5!2$_~GF<Db4lC;o+=ad803E&iz>}g?v%@`~Zr?FvJSkOg4#S;7yEz6#_B-X0ES!$O1X7)|*8xG)A;oX-A$Y}^R
Q?Qm3C<`Z_wJeTq_a?W(d*o{nTY`{VKr;g90<^?0mB0fn<XEQ!k6A!9OMpWG#*$H3d^M?(HN0s~Dmq7;4NU=hnxNabWJFo8;ltu8
U1Pp4xD8Fg8xAQx@&AAP46^!v8y`@NPOZ(?qW0AQOWP{f22iouSnZ;$I(6r(S6G3m0!WPDM4%c{s?NYz$QsvrKLDqnYyWwU@4eq^
?SVc-0G1RSxiSX+mL#`<QUl#s+cTl--utyyJpSI=RuX()&B;=*VIiW3!4(1qXe#JM>wN^0?&J8JWcRV-c<+5{?O0bj-r#Px+Exu`
N0L5F5MX3s(w@wO$)w5V$&#j;2whm(Dy^z+vTc07MBms7O+_k8Y!~kbubb$H0@7@nO~mJxsj5_gWvI|anb|marDfO*FBu$5fj2DD
%0Xpg&EkVIq9Z5q2V>B!K$y!Mt(JHTyu$r8xo!}0?AX}Rm$R|6@vDiWva9i@t0N1<Mu4l9BxV@tu4TwJ;AD<Pr6vtNwBe9v&@CY;
8=#jMKw>@6t5Sp*p8+L7>W;mF?L|&IRXJqdW!yyQ9BW5H;Schm(1T5q4+ZslLkjNb1(yH8=|$9dwFN;01WPnnDmek(7J8&5R|Cwp
h>wl)LM|i!8C+ia54u1jrQV<C=W~6}^?R%c^uA|@_HMz}=)BP+E)bC-RFW_R8whxy!y)J_(6yGd)pV{EJ`sL%tEHvfN`<C^>W&dB
C(g`3N8ye3btnA5jUL+tN?hBs!HxE-Lz`8oq(+JgF<*_j3j^W;qTnB4k<dlN6=zEtY_UN`uM#}Fi>m<}*A+rteZJy;*m?8g;@io#
6LbyYg0Lh(OCJKdMJ>Z-7#9=8-J0%{8UR~BT<fNQkONZfgzTTUo$b5s%|Pb^OU@8SA&PWRS(?O^2D>0iNj4O-?)p60dCbSU94iOL
w#JSow#@IY?k3K{w!o@oPRyE58UYt+Y`l%BHq&;UHwmo>Ctp?$azG>taR}<D;4%2qg(MY8Zbm+oqD$y>B{ldkaF<2i6k%-R75=@b
R$ML4Xb{^1)otKN9Ig$tZ$(%wp%j0!2NY#O?}I^XOa`kiHwoTH(48ubN2s?pZXrK9%YDhXr8^-=ehr|4Kgc!VO7Hvk1|&M{xwfDC
__@}5E9aWQMd!92+tzA_BeMwQAXX5Ka0-LTsl{}kptuu{B(jPDz}Op}wV&H@Y<s5s0K$VHC@2jjH@qMe+R@wI%3kx;0j>4fwrkz?
zSaU3Y!12|UJrnzXwee1KwM^+PP5L7u_~(lcK0KmM{V2E+OqaH?qeMq12JWoAy+Jd15N1^gzY07rZfwuIGv*Y5r`plnxw=ET{NyW
;=}}<vv|@AymZlb&>)y!#ey&t;qVZS_+SW3gANwbODN8i;KF$wpe$Y6?RvP73<8eaW2zpP(IbS3t~YnQ=t}I$s@cVhNiVPZp20;R
#_bFd!g#ao2+#=IYL0G7z>)?wX2gPWB$N>N69tJySgc+61;mn*q))-^2-B=1-V4!KD+z(~1c74l4{U+AYDPkY0uituA_xWH;!-vl
h{B(5F!^g$<R-Av2}K|!$nrX@kqv?(SrsbIQ3j&U<4fWk8fk^^gTV;`R}b#N@#p#>yn()U5YgUR&ly;PQbZ^Mr~q-#c>y6qr9;vO
X!QUsMvl^9J>&%T#5Eu@HUODxU$^1)_R_Xm*HYG!L2-a$14rR%#hgkHsR4r!>Kx)q8p0Kk6*(aU52@qK>+9jq2fPGL#r8wOXT|X9
A~53uflYCrnIX|NVQCR^mI?-sL(Cu%H5)iV1m?;|IC+I*ji}vF&WA1#g0<lytp~<9h0@uW<aLTVCLJ@(q=e6z3V2y(1d|{x4+_n4
NH-o}Wf_`~L-Qe83r*s&$zNMIGJCqbimYaFd{V&nGRb*X%i<8+!{_B<v){Vkt4?@taDRdXyC7mASE#j+S}?r`&n1{DXsJ0Z8Oml&
uf6}~f1%%>z3va;9+2j}M-b(6b-9A3OfLTit`dm`F+>!P#nzs;qwGgsH;__nJ@$^<)OzXty3P;r5=ri3EuU)}xY{027DV{90${ik
-mRyw=6H2@#(F^afVe=SAzK@uzj|qKc_pXb%60BHwD@@fJRn*N9d3Z7qD_Q)RuJLBap|msjIWsz2zXv83DD|2lis%$4<kbis1XT{
=nuMm)=mYRSGV8#{)p>du4}n(4m%IFt*q50rxC<?7Ci^FViLGA2>cTSFC1o|v{lABdsTV{BavbOK_N~g0RuEr#tCay8Y|4m08p-v
Jmd6Y#3x1ZFkSBV<dY3(MetICzNc)bR^!o(f@?UiI)bBr%C-x9s6dI6bC2I$T$OKuM=@K5<%;laBG!_K-*KtKv8AKx0?9|Hn<4h`
0HQ2~_bilySK|yHAqwsmaPOO*0&D~&y=Ks$#qaq7b7Jvo2?#t5hb4rl-sZ9RM^^CtP`{>MP^H%hS0;go`hK3D=l<R&1#4t0ZoxU<
`!|6A$9E%wJL<JUcsKABG1Z42e~s)DIW=5=3xA^l1<G~fT)0qE+1LF>DAyV!{ZZ?9*%MJD`0d)@-SWA%3(jue;RikC8=5xo<H3h+
Z6@$QrwIrePy<LAuUyx5#MI#{5dcz<3_loPxCE8bSqLD&WNX4NLy_CzOQRr{lIn*z4|yD_R@S@ft0uACTq<C6RjTgY?5jODm^n9f
Ae4JU8$7J27-ft)0mb;6NhEM2f|vrfuqpkfBOp;qQ+;!74bYCI)l}C|5iC_#n=Rd?W+4E!0*5G|L<v`fD6H;rOPU058is?WVugb&
Eq`zOZ1T#ys>K0L6TmPTFp%I@itKd_I%+@yZ1&RBq!sswszI;`N<a$_y1@xk%JVnGqwKEaUMx{9)v-?Ttg4Bxl^?s>p&PsH5YJf8
Sk?nn@aR}9ZkVOT(q2Opp+<NkV{ZHT^Mi|gj=WQU2s|CgxsQJBmB8~HxcY!aj~>)>kf4e8u>lpp9u)PO;DI#lvOv;74nn0HFR-Mc
b2yxb*EU(7Q-b$HFsf?|&$%BRlBu7dEvy1-GUXK9R(s72>fKo^j?~J!_x;|_Yun5CNEQM}Xe>Ms6t{7NdugEz!$23|sx2-ru8>h~
0h-A(57KwSS!igNC@bc2FcCqTHz{Hff<WM#8h~``>rz{1Yh_zqHefF=J>y5&Nzfvuvju34wq#$5N3>CDAS*s+hqx9oAbzzH$Jf?t
ZDa-KtkhU5(B<+935C$9Lo7NC^=m`Y>EB{+L-*3{xJJYSik5!`6!*=2FZXHugp8Ljv?ef+=Fszt;v~0V2;~saQT)hfJj?#0O1!@k
(`wfXQ9q!_5t}+n=Q2=}Lx5>0(@WW}ysQXO5lvj2_8pq7fD*1DE&>_tVi2^zTIrXs{-6aPOwh`G`#jHe9S;d4__Cp$E?}%4ErOlk
`##5dwgQcvjD{$>uj}Wze{SgXkiB`eH}t6k)e4QnjPqs_mr$sIt1yFe;n7qW*#qmXhc}Flb^{R!0!~&ccz&lX)M1IGMDlu0gYR%X
$mJakLLIT^{+tKm%1M}!5glm+6($v#1<Z=@geyU^q*8VrKGCI_)Vs&Un`v7x5$gQVFrf<IFw%Jd*MLRtuf0F;nDce;`;gbM9Glu9
S33MlhWCf<uwK@dS`8gg%y`2VAk6_Q!DMJ93$@Jg>9Dw4tBw9c#M@GB5t5()SB+LWR(;L~Q5J3ZK(f2i^)OSKCL2HI*BXEaXyF|1
oBtl>&irs}wVa?uX-<j|X^&AXlsM%x;0ivXJ;$6)sW4C~R#R-D?XIkd%$De+H_U4mEU!s7s6UTzb@rA4T5D(5#jcwj2gHMG)q$@D
v@&oNav8Y7sVio{9`EoqGYr8awA0Ve=leN<t7|J;_ATfZZ1cW(*JC&vIJ+Q9NR;7>--}2Lc-tTz6i2uWMGZ&@+5ts$iZh!45bcWb
)lhmI(p^o^i_*b!y}2nS;OC&3D$Y1G9Bx6hdTg0{@^qlFgj-;&;4Ox<#<Zop*9L9BaKhEt9}JXi2dEqn)qyA(>6W=N>qsG?{+Gq_
lMNF=D-TeWSI<bw0pZMm+fyzHp98eNZ}!;zzJ{%(z1JO~C=4;_icohw)=tOp;4AKjM=tOY70PdTiGn3jBCQq;LI4lQpp}JL?SmhS
riEdiHo4-lHV1FG%m&dqBC(h$#p%QUj6!%&4cMStf>zx3@Hy34mLsawD7Q=k0%?T&lwV@YyP^C>ZBYFH1c8buHTptZ7Ht*#WqOo7
$+IKgbbGUVcWX1f=oJBGvviAiXSKb;55`tV789~)A0OAGAoBF7x?%PYPILe#xb0u)Cuk=S6vcF;!?zlbmNuLtV?CTd;N(2~7wE+)
EKEqI@VRzy8XlRQfqJG*MJl17ZK|2$5DGlOqdS)!>2Sa-b73bEl4@G?#EiuAeDMKZvEb7hi5J1SCvYMJmk4<gl;i2jgK&dEREMRO
YKR-$l}!`>+j_QzxypQH<N?e0k!%63q#uba_m_5v6D8iu>?>^X2)IbY5VT^^p_&Mp)u2e@ApD%MK!KS8Z??9&_PPyp?VWH%QEG1p
RPif3rVQ~BVhI$?k`#fe0*QG;#SfX19Kyg=Ei>ZCh<M8T2r=$VwmKm!12#y3PYB;6;yb>0z63r;K?j=Qd}+u750QX?B?kmL&*?v#
y^`D<WIVIWtl9F$c4U-Qpv<~5_+$VTxvk-<$y<k#LrI@Ce%5sNcr_|7IUBBfJUT4wEp9cfB>_<#${8Q0WWp7379<HyQN=q6bh^mg
KonUd9d<w07cvQ+?%sZ${c|C>gOoxXhf4_o;?E68yYBti`<mdm27dU=oHqDF9?`Zo9_tJe0gDZB8D*<9KFV761B;uYzYTu!jq;@Q
YCuj5=g4GWDhNZ{$^i?>CVXbVNeHNPr-5jV6Q(UfLSZO_=;E4j5j!Hpg)l?70$<H0Gv8(h#f#`^<(~Lz0rub`$HRul1aU=5yt_YK
g;ya1T}2F&AtN+15lV*6Rm^lA$(0S2G|<&IvXT1e9g)ab#bi0ZCp<^6EG&}6fzI*&P-}$uEMOogWHA@HBsL}fYZ13<ffbmXn_hO$
uOKeZcDqzLdnoW3F+R`*|Ji`|R^zq1&#td54$GTbvSMCvHPH3$=uyrJp(4W1UtIkY+Zq1rL%aV}06-hHYrcW8HC?ct&z_G4?*M4!
K0sB*G8=^Teo}BsjacZv(0Ylhxls1wfMEZA_Mb1Jv;AK4k=+(uHi#Q^(0a}JbL<DsY4APKOF-(tvpU+Hv67O}jzpBS8oo<;Z$hvM
RKxKLL%X$E>Z~19t%dKSv_}tNg?TtETxD<<GZUi{1t85>L@7b(M7b43c?ON8jC+`M(t+}@Lbkp;m#C@%><0t1XcG`*)mdC&Jkd5P
00tceAkDv)-mRQ@fC|ip2T&@Qtnv{TBTVyk^#vi^N((U70j&zXod<RRuHHK3({S5Jl@n3@p6~iX4-ZRYIgb@xM!^mV#y~<h;rbGf
QRRl)lij@9f+mZvnJt+uyFL58xV`wZhNrvF3N<BmL~0ZRP6i%RNO)9A+m&>#0j%{T0l5YE6-0Ja2}boY?`{h)X0eh9PI-We5H&<m
0ir&8{SNzVl>kN<EB9Iu<HJr$M3=1&XuWtMqviHe)?lqlZX{PvMhu3JjDY2NfUDzs_8ZjaO?MR7o8k2!X)>t6TDsT{K^mME&T_+w
QQFg99)eXUC6Z5ulAriAT*GEkk<e16nb4JM%0+3Di4mWVc8s8-K!=&bmr<RNntshpL}KK7t<4A%5y^Oic!n%{5Hhr0X51`)^;hq9
^C-cB6#w;ZfQ<lbeEG%IyEzD$QIR2)VX)Li>N0ov7j{7yKsFPoD&dM^oJeOL=ifz&di*$b1T%O8B4M04pbNgS4?^o5#}xkcKW^&<
w{3;x+Hu;b3@j$ZB6?)iLGaM(_*gI(DZ<LbnF64F;FeyzulNHO6%@s%h|@2dW?eHlM?x3lUP^d~=GBo@ccLg3`Rv*3C;>H7s)4-f
EE$924KJt$uFSA!8*tj&YhT#bK2&N_pOx$$n`MM9c%2FuQ&`)^N_){Y3_pR0>tL`pYEGb5A~+qaMH#AdeL9?$&+ven3@SYu=O`I&
p$<Sqa#Z$k+A@Mdz)9FMqE=UcJ7^w&k$#Jd&cN9cB(sHjKu<5GGE=yz!d2m$j_}0L3Sb_9Z~_j617*!PTZ>`%LvKZ&3Gk{~!6AC3
JPxFEU@C-`1gaNT1g$_D!!}NKgnK>{eE~v%6WyQYfhe+2VFOx}as*jXc4$O}D*gsCI#z{MGmP9~D3opul&&%$YUuGq7av#xaqa82
Z~MM&Wa|dc2uKWo!9)H+iwsvIQ-$H!r+HtzysvBmA$B-5JO|1RLBR$)scxfh>i}zmt}FMRpFLbzpGj<<!B<8$2Pm<5veV?}DJ)Z5
=ENByM4U$_ICQFH6GRt0qgFB!qW%Xe!qr*^O#xAT*nrkPkVXJ&&)S~e?%uB65W5|<?X_-&c0KUH8pR#2wb!V`DK~hwG|m!E&iDIJ
{_}G_ki`gQ;rN^j<n0uv5)A|#pd%w?l8A4#Cm8l~FKc!PtR3wVQF5RGY~EKOZCOZ)szv9;w#9DT?=WT$?snl%KntfBiVGkSf!V@g
?{+hJ#$gonxdEQYbQU^tsC00naO43AU1ZQs16qMH2{w-8Ri3GO;YHLhO${sa-|+&GPX==PwXttfUzm+N806NQYaP0a-Yg_a1^Ga#
uf!zqiEZE3^VqLrKXDRQx@X+q2ONHh>(4-38$1P7g^evI2lvwY`$~k;zMdOi>Ns{_6)(I}u+Zw82J4VIJzaagR>*btG<|r!>ZQxM
@~N@8@wpJRroezJ+CZct!x1S^7J@@ez_&wLCB%l5Bu`)=_w4z5)SsjM951x`hphdB)@S`c(1qK(^|LnEfLYsyt;0wg6cYIG(Id|V
EGH1xdF{`&Qx<*iV4@3;0xcQuES2(rG>A9ALrh}zc6bQmseV>D%dKHXbECj%(!>8R4AGw+COKr#Vi5nY+^wK2W*c{fQ)QFoAfgDm
v#vs5j?l-k;SCv~2o{A-V&F<>+KeVA2-d<&!tj`pZCFfPMuHS_eIB-W;;w~I)L>K~O|{4W7kj<uo6%xpOOEmtL}IU%cmEiX4uy(|
lAOR6$YkF-;+b<_VaK-aBSQRz768*<;vyRwpDGqda7p`|Knj!^(1^(B_>Y|c)w*u)E3^?ZjGEh8e!WgBX<I!h_QQNP{b>sR@qo@(
^DgF%FO|)i!bw7x74z6eB%i3o(&6NHn|6~n6REI>hb(dx+h*=Fe6K<c2uJ(nuI+V;gScK>J6R{Yhh4p&jqCu~)((IXk3nswLP@Sj
Ee0_LoQV56r~u|UX*cKC@WiXFN9kLJqd)MeNwq?>S>Gv1<F(Ly5}H6|sSE_z;2!bf!oz|C@HBJe;OJvfNjM&+CS~UV0&WAhNk<P!
Pc`G7z$s~`fiSEg>mtRE!zh+iVH9Y2E=km}A@7+Eu!W@5@QIoL#$LGv;v(*Xu+MUMI$Kw=(p}wLT}_6pS~WFO-~pA5I(a;ok8R(v
fie)4NR-AQBtZMP;>UmlXzBtm_BW|TxFYnlK~Hqh#!YX3x(hJd;4a}kDGxSKL{%KHZ4`mLFS1g+N%{(i1PW7cvA58BXw9$9Z>!sP
yYK4Q#dXN%(%;KGU0jJh2q6{Q_}m0yL#V9D0bPvtdMF_;W@EwS+}6d`$#+0)#=3`~09Dsbp0~Yk`?=lsO5ZF0oaN`J!!v@x)?tIq
wqY;E)_%kKdVy>Qx`?~r`w_M$lKNOn55mJ6L1EfTy1`u)D%Lk+n{nOZyqmLt9``S}I+ZJyBV^j;(oQZ?%tCP^xn<07;h`wGh(ac%
@{j<7m?!e{)b6twJ6pFHPlcI|D(IEZIz}qp@J=`<z0+YN#-awmgab(`@Fe9QEEWC{w1QCJvBU{i@il5sqLR_P7z+J#?y2u(6!tv#
`5kuCX7}-VuIoHt@H*so_5%-E_k+^ziTo6Ta}cWZq=hKaooSyB2!W2ec3NM9X9i7?5c*9!yv~p8?|}Z19wX1Vt?R$6*T}U3pB+-_
Btf+eP}P0S`<nL6AG<qGd!Fik)b+^Y;^(maptg>67j5OWu~O#N*nOz)p?|u3!gAVqRZ|rcG(5!BNNQ14gO*IlNkO7|TJbO$B(rRy
pd1Q!p*AaEEVI`6y2*Xl*XcflvGQ}ZpR12@J1QxM4Rqm_3YK8^y1v}?OI&4CUE&Pm^a6f3z}ZENxxs;!YRp@{Nd+Jv2%)PD-_kD~
F6j=qvq_dk7v(KeYEhDDHi<z>RQy35Q6ft21R`DL)M9|BQT}fnF_nqJ0IpS0D@Io4x2cFbFNnSjwYd<S$i@M5``eg98GA4oJv$4N
V9;iq4l-_mhft_Q`uRMc`+{eGj`iBxv-caHYpr|B2ZHFW(T+^bFkH}Mr9!XI4crlA_Tz&1d1dyXtOmT16NJE`NDu&9_W`Q)*Y~{y
Rex>ZX&aCOFI^|-ZF|)`B-6HzrxTVahksJ-A|95m(>@P?M2%+GEr6wUUpg68h!yJjV8p?+8O3}OA&H3aBC?v7>rg+JdfM_NKx^4G
Ym&l42Sg3BQq+DmOT8$|q@9JCu=GWexI`i;nY2n;cw9XSxOMnFo#3}rMePbC`5f_c*6*>t&?0p08*IRAeE_6C;yQc(j?^g5=I1)8
df_~8DE~+~rlhUm(n#a9cgh*Oqgf!VE0EEPtg`~HHf}c=6SH!b6406@9tLkzx$F4EiwTR3uXkataZlCf3~w3Y3UIQW$k49V;<nM=
58R@Q%6UbsMY(F2`nBO4$v+}mHI&dw27KbF$U8uHv~46$>h(OIF8~EPf(+hnD$m%5TVDaEo@1vr4Y$%BN-fdCS_#KiX}1EgM^3P}
$Ql3Iw#V8L4-RPI^@-hykl?DoKkGVFdizbD4tsyXo%{CZE)Qt1{(8E>a-EDo)!y5E4cDbVUv*w=+n2hsR7oM)ar#EZA{O?{9fi)|
7GY-%Az)@)5^Wc2ml$VatxbM1za6pG9r$LJBqlFuGa8p?Tp@;qZ6l9W^2mAM@G6UEi(|}lodGS5MGkK;^44$*^w(39u`I_fKUe%5
_4CVDf4Yk_*y}5)Wd`yISo+Xr-?`;@q_|mtK{qZtmvNzxK5MEWa@;guw%8CG+ePV7?<OIuCIBCwOyTo^j;K*`MtG*`qWi4ZS@%V^
+4R}23t3-GTMQ^JGdM7CjjhVA#_i4@A)GM)&l{ypJr#f&7xe%bOnW;r52K?nI**t=Q)VfYfVk#75OD<jUL%As5XU5aLBBWTPp2GH
&G@B3U|>L_7Um5;iN?X&a&X!xo`R_f{#TUf@Mr|LR9Zoq^m5$~1m>Gh4!Ord2Dg|<M|9dyru1Ne087x<BY=Cg`pBb>jl~y82p-A$
xz%fr_v!D`UZ(+~?i<cdz_yd;w#33H>`1hMi2%Z8p&|t++%1r+lt^~}Fh-^vMZ=}?pVNP;-1T(%<rBqWS=UQ8+>9az2^B(}r;EUK
G9%GQr8Z=6HGCKwg|d*b7Lv28)MZ)WbH%#L^VB=l4#j&buU%_?GpP4k$t{Au4r;jqS-~CL9V*tAWvMfa<#{OYiN{5D<-4$lj+^w2
+ZF7<Ewn5GKnh{;PUoSQgbN}<721hPe*0{;#jFG{MYJ~Sw&)5HTZWBX)~G+QRl24fSPO8vYJnR3P+w2IN<MSiQ(8l;9vBLdYF??6
Ila4giBi6}e9%VV3!JXe3pI`1F={tnmRSfsk3z?{5)u#K%WU9H!F|>^>V1{YYJ@IYa-8#$JyoI8zL8APr4)cts|`R32Hehj6loPV
h-;K3kl9Ro`jk5@ExurDZ{~_<tGBYQaI*P4;&q1W^yd-I!=D5vYMLmGx}8EATjG(8en&n^nY4C`rm&b45#cH=Dl?g8nHCr=&cbZP
N#tWwl)EsWyZt%r=B6jhPm-seS3PGjLyL$}Z6&DeK~M_<HRjBWT3G=k&M9%o`5(GQctl;lc-cq=#Z<`Cchy!^tGo{Xoaq9`uIb(J
IiV|X)z<z4uQ%EjKG%Nk?Q^V8%?JFEkib=#n4egjMP5Xk<+{M-i8^r{10jVzy@n7n)E5dsBDM&f_I+uWuFq~;+&UY;DbFg;vdjwB
m;poq&Mw`i0wCJ(BjL&;E;vhlcB&+#nl8v8s`$eDgdA$4vYm>M-}rnRS)Dg=gz&WF^ba}n-wl<XP)F~KTOdr}gee8a0!XZaN5=s;
3MUwFqIOX*9b+?S(OD%%E3v0uHM1;>cOJ|G3hEmP`**_v`YqH>$@#X91G3oGG%Sw_+mUH#>ss(0uL}xX><3$S>U&CMG>bI`HwUQ<
t$=`aG(M7=gG8|KK7o;kPgJ^Sh}_9^<|;7-IhiOF2HqGo>AsXjZZSpnbGxUrr!GHLo@Uyh;U(=~BQP9u7-p(-U<_wKBhrFrq+T9n
y%1D%y^QvDKJFJTT7>(`3T3&3Dsy<B2%T9hysx@<y(2j7k@^l=-bPv;K7Ca2jh3suQ}4sRp26?hT-qK?)rp9!085itXSvPlVCLj*
X8?>U6Z93FodtwW9uDTgPOyEkJB}AuCsSsVC!HohYj{RscNeeRPI#77&X9H&HW#6a04hY9z}3A2QFu#a=RX_n<Dl>ya<@S>JvRak
#8pM`v3>v2(E!rF)^C6$MGwNk{Zu~yy#_VmTuq=NM-2c2R5YG~A))~4uxJ@>-*F1gBk<&02setkm7?ZGiY(7-R8lpn(}vZ7tI}Vj
;a9meM4%OsAA~vScBt|Ae8h3i+p%mXG%yD>!N(0OjVj{;xycP-iDFPhFO(Odo?1=e8-g`6OZ&R5w?Td)6MqITMmE!|13TT9{W%qI
^)38z5b*P+s0c7nE{j&#GPVx!sT1Pe(fODHYelV%N@60yt>6%iTP-Rzu|T{U3i~Y&UL-1)6^=a90#&qjzYSb%16SMF?%8X8NN#l+
m4FZlVneCEut(XO>jN|eL=8~E_C=q}09wbQ_Hj>t!8Y#S;OXd*z?A{CHu%BW_Q|w?t}>JFgG)U#yzow8DW%2wS*Za2Z0of`?~z@j
x{0Fi?d|J%#Vv^wxI6gl=RQBr`CNxV*gQ|mU#UM36+BR6X|@JU8koU6t!7}z4zC9fs5pmg2I(bgdG(3FX7Q^rPJ<9d&f&L5jye%=
{<WbNCn+VsE2T<sc|L5%nfp2%-@Dm5th|Phpb}rv9yQ1+?YkMl9Y>T0O@86_hKQ2uu0UBf%F$j;9oA}W<G&D6Zh2EMV-pDuTQW!^
a4E2_;3}v~6Yd<5jj%L=gsWMMF&e<t+9gre%AUO3jvc_2T)KpSA6p<}^(|vE$<`n#`QG%i`|p*{HKw3SwrdSNBd+nI!3u89uYgcd
dsEkD?|n3J^l+}}=ow74zlb73tX<FEAhdqY{l+45<}CS6`7riU=2qsz^}Wc8sh!C-u{N_dEq!ABy`6bq__l~`5<3CxHL)-9#1nx`
?Jn(iX;uN>3NxDvXKfetXRSBc%S-F|YuiW<{w9Tf<ED|yrgYPNLJHylPyr6)5Kh!%`PV@LDE-b0A%AB9FsN}vg1ut#K}sorr&5%M
n2(C^ONz9Km2f5lNK6xZ@fTO1JiHpb1fdJR(i-=0#^D!*kj8q-3LIw`1xS%NiYyKiqbeSvtGMlUKlE|R`;j24^Wvkgke9loOfz^q
+#I#QQ@u6?{szXi6K@5#vha@_u5c8(Lc`0kS#1(^N#@WH+aO{OzWFdB9BoOJxhP#=aE0H?e-3q~8MxZywDP$_J&MKgnHmpi<^v55
`Z-(maxea~x1Jo-C5i20{T%IkQd{V-_2<EH|6cWTmgmg(L14SKJa9$OI;ixq;1-wXe#?5d^=jn;arO4?{dE2WqO|!4`79iE%s|o9
r@7C-5<%<N=4GAPKH~ub%yx1EmV2~;eXRWk|AEEu#Bh3l;ALaF@karqZN;CaG}^DTBTyZE*!rd!w~_Gq&0c;#H*OKrK@VVwP5=3a
tL&Tyzu*{GAAIHUvvcrz0MoHmg!Vbwl02+Y#beC)o&6Q9L&lSc1+EYV;K~0P!o%L#FYuYvT0BoctPle0JZ6d^D*W4ij{M))8GCnK
DCJN$giE7K@qXBTEUmLbO+DQEB?KO$4CG2=%F;UO+%ay}BUfM?kS2W)0J5QmK4$$4PRmWyRh4y2#EFXfnuGk^4=+knGLzxyAqgJ^
UfkKa7y0w}yYVZq%ky2cE@pCtP)&^Llivw2pS@lk0UefvFW!<CdiFm!{j>e;arj)@=jz{kg;AZ}*`6H=s$A4JI*bCtN{z!S<s6<?
?&vS?E<1q1<qbs5?4H>*Ex^_GXX`XK0Bo9ZfFF;UofE%iaWeT>|4r$e<2Qv*3f~g%9N=5O2tV<+YN1_ANb!wu^(v_ISCjX*DSjLI
XDFz1<i<bG{yYZ`5a~-A<V8S&gR<5D05OsUO3EXegExcsCkmpyGc25~Quo=3SIb+^y@Hf%@FW=cXq1DW1GIv7DI&Ur2!oI(9S=tc
4?5V7lp5ThLx4MeWaD3mqhnL4fIyWthj-dH9(yzUpW&|`2cYHeTOWsL9THb=yQ&Rj#Y>T;m|AV`_`5O&`Y~nv*0%0iwG}@G$QWIV
#X(7;cSAF0I#sFH22iWNikr7G0t^Ze&iHN0IwfjkcY3-H`|Ro}>`vmF^<kE-sF=`m>f{>j((@O5o)BxBqZYU=vSa-LQ=R?$YwLIP
ioWRjKIhM`jY9OBYKEyj`9R#)$@V^mx-{JXv$x0UgF{xSN5bSs>5tR|t%>c^GEg)FVCOVn^K#G2i@JLm*jxB5)YpekE#Ixt8>2}?
^!C2Le~VfkZbB5<`68-Qly|&!<GqcojS5h~-vLWh6n(AFv*#3EKL;4J8uztaN4?H^9r@Ve(fwLMM+VX{dJS@-_Oxrg2ciHckX7^s
Ld)u3m5$c|R01G{dzBo3fp8K-S24O3#D4R@@t9b}Unh$f@YX5BONh&*1eb-FuKT8l^o7&A`#f$DU!ObJGGAx9uXJ7UJl%1)ZFB1y
_APH~*{E`>)RN%Y3&~?g1*JW&4bg_`#qT|BEv^NDhOSY!M6zdHGal3N>DEM@J)kUNKLuTxvmKpep%&1!1Z90r_iS>H%boZgNW*V>
DSS>e%81eqfr=(2r7mkaN<3S-db(P?a4_thD}{^r{Rb`LwDafl+V%6jem=(^%m`^TuVd66e~)@6{c-AR#Mg?C6^~*Mn?DO|xfft*
zNhJ#<_Cycme0aIOnf9BZ@$*T>wN+^DuR~?@Oas4`(7(<f6ncDy!(~wvkz$f(bV~es6S9q^6*tq$A*j2prk-GkVX(v&PX8Y*vh`f
V+|0E=jwaWEhEki=UzTH!3ob=TP_ex6w4@0bG;;-9_$VGNJvrZj~qD&Vj(kn8B&gPzZ3&$|6DCp7C;3lA`lOH7if6dxF68s0uC$Y
QHD3_uU@8F|1zHlK>oJ;MkUohJO20MXuDX)b|JhdoOH0b*~f&YwSsAZJ>uJ)G)&rx&rar`0X&GthIq93PV-w_NiJdeXc4Hj8b00E
?7Ufy)qF3r=jBYxH;Yf?V6DdHxXe@xzsx;&fND*Cjc!ejN>zd9;*UxgJA1x?tI?b_t|=L{YrQSW)IADZ-2+;G_8%&PB>Oq@PqRN!
eEsru^N*c>%={J8m(M?9{$cZX!R_+p>?8TtsIN6YaL2*_#PCh=Tk^NnpSAz&>(9Ge^l$%&wvGO?@%=A>(1!<Xgs8Xm;JFD@(B!}d
L?D2K&=sdQc^l#EXsZQS@>}(LBimZo*92+;v*8i|8W2v3hF=Op6Gkj0sRpQEe)RU>R%<zg6WOcAs5W-YU<BTXo&Gw>2W8E`j|)jE
^V>?kjCmOnPSfI7j0?(Y?a+f85!d=A7e=|l+W%{#+v0C2t^cgP2ixC0)Yp?jFA3qrYa8|Z09~&_jxFe*IdzHF*lK80>Oe4~1_$tS
qK`;>3RXF_<gh?xJ)1t#^0TT>5r<n=F*m`o;C`72R5|?53fTs~(DJobc(gH83a;=MS0D`>zb=oc<A!G(&hh20U;76w2>$YOg-;is
I(^IZlcz7tPhUHI-SiWtpK<)7=O4BF82MxM*J@%a=RQ6>A$~%<6EszRAf=$s$=bg{o$JreKRa5Zjc@8fp!%c@nEd&)mV>w3N@o&=
pE@<qQ~M9~6K3DWXNSMLHn_qLB{RH+iGF~C#<Y+Qr%{=L3U2VbI$9YD94e)<^l*3d7&ydn2WhG|InQW1-u$1ifN&)xZF>xqahmTb
&1k#UlyF^`qN%6K`#3WHV;I<R{HuXEsEBkOTg+7XIl%L8L#L7b!D)c!H%`Y=D#6$2X$(ax>uWT9Ah(8iHkD|+5!<_CK28+TS50-a
%;BH}=M@h$zGgmF{quyY^Q$dCo4g~1hZ~<a$r_uEnvViY@PiwuvZTGj^3mSp`9CWlu4llB+LlK_>F|#PIhp|TI!CDDV|!@(1{g?B
Pv1R1hyUK@dyDVQe{S(}$)8jH9O8SDeOCUh{Nt8KOpjzAt$w`w3GoYy=@T>TN$E=I&aixy@@utTjY?Sm*+3N48UB_U4zj|<_yYF_
97-G7W02KYyg0+ZOSqP?DI8WTPXzQCnu^F~<ee0_M-o2fcjBUVrXm0w`75|Zn5P{XWyU~X7!Cj`W8RF_80z$2O#SA>-t-t8q8Nj`
+`{AtBB8v-q>pI<Wf3nL15b)S*Ktum%jfa#QC`P+4mvxi0JOgt!@>VNBgp{TL7=_JoZcZ6wDFxH-~pDV*4Jcfv@3B-1XCfdH)5&D
<0;f~S;xeRw^xID7_k_`7>FdC<|&HL89%4KH}<UT+r(w(l}#I)H?e%r_8JNAy*^{sD<l><!9P3b7DyxP(QzLdtfzY=FZqm}8Y<9Q
>zTuq!Wryl<(=&n^dZ?{*ctg}Q=e0PKl<m#e1GWn=Tw)U4>{k8L4!SBU6S3B-$s9P`sw{=U59lX!yA6!(Q184y-Ouf)%q5!{@QPi
^#5?R{?(087vn{%9o_-Rp|&-kD24YHh#EEGG}sne0%2eTR>l-xrGDc$HpX87X5b;<$~(v^p#-B%K)`Pl=+j(T$+e&vL2o*A`L_u)
{U++i)Yg%@AIET!fK5OcFCf~vqzNqYr7!Q3L6A>fpww%OcSRkKV_aeKfrc+3Qmlx?*XKCk_b;HU_unGF|5VicRcejG(0?5XH51cP
dIXEhG^eT+!SEV%aZ0l(S_Q5K!~5uIoGREEM3<ouAV?>8Lq`LKRIm2j&3(#e=TBvyz;HGDG7+x6`_B*T_`w0}vwffSGtvm3i)L}W
X@qN~wy%M)Ff6`lt8;9$!8e`39Y&p6o<?n2JkecRY~VvV{Y3qB^3>B)!B_I<M}B|!_u(MVPvG|g-9Fv(bc^Lt;*sLw>=OJm`pM}F
MD_mZ4WRl~vKuFJ7|=D6>c6&={TEcjMmZei7O>8DEcSi$3lmL2%Yv!0cQmhI7_b4wrN(S(7zk&0KiXn8uS6e{lm$(fTJSg^%4q@>
VmWW9!(GWSV0`qdEc5Tk-`|7b2j88Jv0)A8$b_U<1|8AlXwvKm8&#y4R#`!JQ4)1@C4eFEh7%<IDB7l;Q%60RMi*~s)M^N{r!YD(
X@iGKY3iUD>avc7EWCZh)TREm`_;GUkKl!u#*2=5;Sg7qCgEvP@`e|Oj|oOKW6Q}v%zMK$UmTGr6qh;=_gwsQv8OTc)os|J*(RnB
fJ9w>2ied0|FPo_Y;bneVftKS;@Q}}JsS1Q99TZu?h2q%x6{|KU9f}Ax8{#SB&bd{?R<K`T3y`h0$2Ey<qY#DsoThlEeH&+X*!qb
BEFKhmX{O<=ZBP!_W;!gF<on)T0f;c!w;Urj$wN#8`;~?QE98=%_=t9)`he9`8=Z`owi>5i0K@B+;CfzC>WxMoEM^FXWxOtG$4JM
@E||@oEf-+Z-aAFau`?!{6a7zq)AS2dMAdBfllPr7|pVyY~h%TO-aLd>>-JHVA8wa<OAfEKu{l3%0f`&h#<i^0~7#DZH(Sc!Qwgs
y~K@FIHB<oU_paqTnn+syyp7$-Oz+E$nH|!N#Ot5`d~CKi?UH<DpIrmYl3d6lFugUt4^bRd2NX1L<!((n#W~;w+1;0uBKU4R>_hC
e9-4+Ur<(FE;rv!9BRIgLcDY~0?ZAJ9n?umcDx2c`x4|X*!SoDe4p=qefRy!Wq1BG_LAln=22z`7@~QcI+yto;sKmAzXZsK?aKnF
JXQioyI(#@e)Mwj>E;XY^B4^XZS%ZO^ES;pW0xU_KEXZ?znVABFCVDB>)1cr_H7+P{MGQ}4F|NgoCmbZ7>@>Y{ZZC%hzQaXi3%(?
iE9Lf0BRZ)EYw#I!ha8zw_IVQo<LJ$l&Khd#5ByD^JUa9{BKULoF}zRhE0Y~PA)+)FIh4Y$5hEmRo;__&ZohK%g|I4<*@{#sp-K}
+8sX6Ai~5ykEj5T0?K3XZ3J!^u_{ze0YOn6m(@g)fH@JYr>U5v<=`bX!Zb@`1w4YU@_NbZgaSJtzd%_gQlj%0LV@ZAM0n?7y+%WK
X=reuA#6NE=KL6#8zkOIbN3#Sot2m<Nf&IaE<^;b3!zI+Yg6CHK0EtDXvO(4xYqNzrgP07NUVDd^SsvAKF{DNvV9mSbE>07NJ5Aj
9Hrf%+$sGn{l4%+i_6Jf%paw0F1LmCW!X8~7#ti(i2-kyTAn0N$8W_yeEH1t4W^Rvwx&%}omrW99lJRz$O`E4`Wp>MtWQ(pY!Bht
@IEiH^Z1@SjqgLGu>Z4tY%z}{&$}nMj+TKHtVMqCK&XR7=W*$APG<eTaz|(x(8xlQ4CRX=_D(qG^xX$oun-kg8K3CeD@^gG1+$Xr
HJUB^tLGaEvuDWEdyU<T)$=om)p9@j3&!YsDg`$*Zk;lqgA5&jq{i%y2rb=4S2~T*aM@GF5?025M?5RMrTN|ws793+1qXP0fG!ml
n(RZ1h}yz7YJMQPE?hD~*HP9@kNp__BFYn@miPNRhAm?ZH4jMvTC~L&nNN&{Lfg9LZN=iFp`bK19@x$_qtR$8LbhtYcKx|Hd7=tF
nQk*dc+)_tp}oftp>-sw)?cr8uJ^IQNESj9#@MV|wLP@mq+1oxm3Ngo2U&?H7?2EfQD?GFqRnFCVwd978W=m~`Ix4iO`mE%tKSX(
LaVdog!|*{v9`@~nOK}en91VA+QPwICttoneUm=ryaHV_YtDmzK9t;`I_Hrz8`F*cXaD;V?E1OR=iKR2Q04Hb!rB|6kDhVKu>NQu
uoN^8pN%1(xKy~x0sMwQsaFJ9=lk4YG|TH4({3TyMp-*$`*+$!qP!)Q1XoI^p6%y^%T`@YX`w{4<qMRFRXllZ6^)}tbU+G<CS!vZ
fGC^cqktls2q<VUk&}sz;c>V%0vJS05y@3kfdmcT5V(Jgt~HQhkn}!|{p=y{X+F<Rvz<G_mixZeeao%U1U~@g7gTS<BY|r4)fTFP
id6)f!Zdo>GL<Ylj|gYqal@S+-zgxN3p8d@tJ%sq`Q_)a*SZY#KHqj4`^)cU&Gs2%^gb6EPTe_z)@@Akte!TDs<vGNSFQ`wW!PP#
$=Tc-+T78e&a6`BF|eR6wsXA+-4@Y>>P+;B+#Ce?uGmxDPRzF8$BR7RbSnjBqq;2M>YdUuD>v~(<qd2H<2muu%@g>(OzX5%(3;YF
0n<YM5s<#mXo{h%?DZY?^V;Z?`B0tV@m#-#AF1;2+GuoA4MYx9i|#rC-tDczqD`Oi;GMc`&h3Teuk9=B{zKaP<1jGfm@-63r24(u
k=3f_Rk5x)&2JIhOPc-S6_3NUc^Z_hf`>1LR?#)lz$*Z6kg7tAW)(FW2`Um86BiYHkr>qxI2NAvlH|Y}jmR0!k;<vPu_I6gCh@rf
)w=HkUDpNfqN4g#$^HFJd8J|0^mPn%w9}R`#q0eNqP)C@*Ngf%!`5|l)NH``1fJIlD`l~AI=lJa3Y7J!;&9WoXGDDW(camNG{bx+
C$hCpW8k3R9Q7DiWty_9a+TYrXhI4=wGpWFsm){I5UFGZ$d2^gFk$7PF_UMRCsmnVr3GfT1t=2RG(kQ++4Y5XnfHaALSAs4S^+{8
WJN8<G)j~9-e>LTTOW9vp~T?6)g9HT1fW%>B~DA?qI(anpuUU&u%AD4{l_S=_HJtqjGcqQ&bOOm*dMtKegmA|j;-e$2miI>KlXbM
k@@KL+y1pJP#$S(C!lqAkn@S<;KdP5(INm;VrgF0prYl`iV}6r2DkL(I2P^<A-@cC%fsJ<c26}mG_sHqvx+OwmsPm){f-zzLFzoh
kaz632@bRd1?K_{R|Vuq{L@a*zLOmg1ZS)(sVtf}+Gny~TrK~;*=ij80xaOx%Sa<k&fWHkFb6n?T$~UEBS=hc{+{Mq*=H9|T}Fw*
=n{R~W5+0fmJ5w=cA?=`yCTi1{VE+*&}o{uyqUJEcyRqlb18iYv*Y~<ytel=)5ll(Vg~9$_lu3QZroH*76bW^FN2={scwgAqVgDE
iLX+f)|^WBg@@7Qu1NkE+)@u0m3yc(i?*;;vMZR&82}PuEKc<Ju*d?vm&<p|*&aX|`<VAQxc+B9bbEdQs@JaT85kRO+{bYtBzcWQ
8gBn}cmA(^_#C}3|A$e2lFr?jht{a$Z&bGIa0hq!Z0@RN^QuVJ4FIMgy_)CQ@dBC(<mur1N^-4`N{3Yl7%HTMJeK-Rv(l}4gNTt^
<Kv4R=JEAexVYjqpbznG^Z~d^G!#0*Ax27nnUZMEcyIj}8$-u=rM8k!jBn#MO#t}cSb$#}KaTHHn-YC}0}sBg?mTRc)N)`9b>cus
c+ynhE2u0^9bsb);<O+>?S-;CRG>d*lmJmpnoav%L();BFK~MJebW`7I)z0TxG$<LaDS<(>R42OHBJu#iOC?G7~dU)zpVYNGE;To
ZGk4Ac8K<5Pbr|gDmgpCMq0$C!E7>*=^Kig(hPzs(${oA?SXKPcyI-GY4tJc6i{(+op`#mlQgsRTq9UHJ4KFP`W6YAGx^q6+$-5d
*3bWy{EZr|(F^>J#W*^hiv71QcwO7uBm7_c9hLAqsA|~u&OsO*f1?k1v}aLrvOM?teag}8ih!l+tLn3;tLX08nq^HI1XZ&i3ER|Z
ZciX@m~5b-=JL0|aAZAxzh{KM-{<waH3VGImm(0KAvQ#`i07tJZ?CC%m1gc!@hVl?6FhZ@vDWrmfU_SF(4w!8fgfzsYmp2;&KcI{
(wEW}x?Ne_WUadR_3$UyE=<%eWvIgwf#Fv9_f*fyud+bbQK3(%Ic6HIi;v|}gugR!v-z;42_L9GH11)gDZDc7G91#c)CHp&a~lol
EmkHzd%47{*Fc3}862-zP&5q}9@w}=C+dvg2ofJ}PbE)8eB|J0HrZQ%=9o%SS2#^-0R<q(sMG~|<TWT?oM`P9>c3dIpukg#b>W5D
F{GKan(+C?V-!NFeDwYt`@gNFbBtX&T0Q<YeSWuYN14`23DtMFS%2pt{5BfDN$m1#Z|eGYaMduHb@HDMzy8mtWv1TO_VZbvt9<YD
IsLtwXSI70Yv4zPx|X&05a0^kKvbX^a2~#F>{Kt)zqXAxWj~Mn>DX4H`^=~`fJ1z9SrF}>M%JsL=l{MBkM^O&=#<fKF;9#%;ffky
$F6qS4_zDY8|&NB*QKotRvT-u%3Bc?Rz+>FF<>{t8(ynOX;E-3hQ2QYr#{8ybLwYhSDxR7cOa^lUSsvjCmp*hhpAme8kZ^4>etQp
)s(K{M$K8S&~zZ*RoPt6GHLdXO7KQEr>hkal0i@zc-6A7#q-gUY^jAvoX*|OBG5Y)zD<AxSjf`ET;^yhGqd2g#5AB)s6&}L2Z5+%
Ok<cvZyOt)(NS*~Kc#$>ygA?JrP8zx{L0}^^VuTa;>=hR8qI&$$^Fr+@6jkkHasJ_%X8e4n19aS@5=etZAzivQ0AldX?yj__3QiA
-?oeY)v@%yJI8N#y5~V~{Xz8FK6ic&_iXlV`pU9fmJL68j$Y+tR+^9yI{ZY$dj<?BT{i!BZ}BZaoX2;CjIZZ|_pAV+Q_%T^M7w=+
yl<NKZMj0|IKJv~d24kveZ_;O!q=EmjPEQF>hC!Yvu$c!#n$=S1oTtOP<|rg)wN0np{Yob#mGXSa*bpTxTwgzrN&OKW~t#5r@hN(
<7ZyRE^E#d5>bYAjeT{s+nUFB0d2m~*Z#TET%|&IM7>a&GZa@ka2iZCjM`bJ1r(AX?Y-T!%vwgHvPPh6Rs-2iV>$w$rK#~qc4;r?
FJo2`R|1g+UPRE8LB~0bUx3kSW0t-;RpDb8KI?_qnb`@@8n+8`3^*hdk>7;IyM*ZTQWg;xETGqQ;$bu%1W#cCD>;LTE=ct6=bfAM
Ta-A;e*V6U;6>VReeC<KPyY_a!|;@SD7W8wv-k1e_kK#z?El8pkMGXtv@iCw=g!~Hiz{<waRt5_Ml&0oy7qdkvF0&nJJOdZ(Uy`J
Ux4&}h1=U?_Wnl$uIZa-yy1nm^JEKpr2=y8w1ECnv>hPcsxaKrKGdix{8wQ}<rX2>5FI=uP5YsiNgCF&b|^4eqNMNbiX_P3N5_{g
`Vu69K=0<5$U;P1(JOF8jh%YnN>HH1N?3j_b$9k|8d04fcrj41>gLzoZ_W1ZDoq0qH9GpTN$Rv0iK1ayR<~x{vseZu0VH%WepRX{
nJw*EHNgV7%jm9D<G>CN?1k1$HP?lk-Pqf@jmySpjwcuopjt#&M(zrR#|!2xvsKcBbnqB~goT-T`szs#7qubMj|jK{>rFxS8wmR}
P599;P4ia4qCAk3<o^FD>}|oM)wQ6}mdMD+$jHdZNF*{cG7=dXiHt->B9TZW5{X2%Y&r5)g`U}apYOZ(?xzli?zd;AyD8SHm8>6f
lI{40J|sw_^Wf+K?kT*Pz5n?q-I}eNKkxN@FXy!!XFbn)U0fgjO<&x8u0Ix$jX!PbN@G`B`ukUsElB&h>*q7wXSk2y-rP0YGnw7X
ZBW^~YD9RxZVSYfpEK+3;n!FRD_fD-gMTu&IOJ60hUsxZb?W8R%i{5+8*kaj=_y)l>YW_wS{1G1-jjZ2bq&J+#~nGP#v>lE{Sd|k
3b4X@N@*^AP8Jq3kDvo$nEQQxKKJ``@7Foj3S$LQwTTzLOm-ge9$o{dv2+S|a<4+)ohwY1UZ!=OwmL4w&o$Iz+_qtczgvcJZ)I#S
K2jxxz-3sbu)-%UVIAFUA++1|>irzzDoxU`X6zNZJ2wdt!5Rxi-&dhir$7}PlY-)sJ_*NIviFzmH|bXCXShxs4SP~W*?83%9HUa+
u`fSM;+%jf<GSffx0WT%46=Va2Ov9$$JvFM6WuiXSP51pv8M^xMei9p9oo;1<QS}?#XC<>0sFqce|Jbf_X?SP9`msm=#Eyqkmm&_
r9#T@3wx7Y$9e77ec(I4@8i0*8v*q*(1&31|Ce&))%-c9dk^npxEB3h%zM^%(yTb}vU>Rg-fq05pN8$Q4K16(%D+*y{|BiYzCpG|
7twX2>(ZbG({?ADo)_X9BtEIp%nReb0rN4YoDc^3Fml?Heikfx_PifkV>eK%*2LKlBchiJchKiIo33SVzHtX0JH)!+SVXS3bFgnv
e$Y%3;%{=^>wO8w>X&INp_XBW3BsdwD4U<oao*DsT?P%LnQYJDe*6ORickOw%0k*`7F|Pa^|4BJT!3j^hPcMO!+gP#v^a8yy62@d
>18MUDy?GAp2EYWhFuS<8d_bv2enSPJjL;@8pev{-0*MU$S9!y*;<J+Y@K3fD*8J7PSP*7<*v}c<^oC%hMQYG>v}s5D|2+O{*PLn
fxwR(^aiva>})hp%BjE+)O}vTsH5yh+4i#T;8Ljv`(UQMM)o3y=3e`4^ZOol2FGz-AX5^1`ZGtfJpKJ!I$f<9M(^6j;yXmkTT<`E
T}575ypuYUzE}TqA#MVxd>P?|d<-lb<63<8e`IYn>Ha&b{bdy6lNK$vF%aro3-jcO!IM4<@~!%~hr?s2S{4s+!Etnk6TxBBIo=5&
PSPH?HNpmFD$_65kz<Me;T7@5`OgPIWPy5Q3hwr9d3Rh4<Z?}0u{qn)&9UPyDG*T+M5<?AK&LIO_@HoV+DyG)QsVcu;+snA7#8hj
3EEhMYtt~U4soG{^qxZA;&gy!E^>$GWpbZS6StSmFUR6hVT;x|s#I0LKO81z(R0KxyOqRQ#!U?)r>TsZ<=k1?NkQ|2U5$`NrNA9`
2)v}Y+L}8K0R&n@f%Xi}J3bth4nwQ=9fkLjbNLL6VdG(2&X4T}zuk<vbU~WM*7+~mm_jK9H}=83#-%M!aL)a?gmWE^y+00j9`4xf
&IV+z!E(+`RS2LefRn0o#&`DqY;}U%d^!2*WtRti%<Q^<P4Xz}eZ~`Ec0usN;U|7@a9~V{X!T$JWmMx-^Nq3<<68^zsKG%m!P6-w
eQD-7aD*p&r$PbQOdpe%0twA=LdHO*a<Xan1xFr=HtLB5tN833uoUw+Tt{W@!NaKg_sEm$4W*dUb>RFa?z_zgVY8s0egCZcdp_<N
_hr56dRN?|3%uT(5gG4378_=tm}4?e%M_<MlVE<_5D4m6Y1PVZd{zD2r!CIsv|KLMo&z!$J+9qQY(7Ai7Yx#XmsQ6-3i$6S>oDm!
bJR1bGIILYv>|roH<1+R1UCvEBH|pX80J?$cl|5@!~!OJGa<%Q7JN&s+<9WF1_$=$SD#xAbP<j(fF|@HJoiIV1cBAqH;HIWQZ5Vp
RR2Gi@Z<bF_{|7OJ*@oKkjI_fH2evi{sLOBmSYE_%(kj^mFptb^##<WtBbBI0_SYb1#V4v_p+*WFnGO6>hB}I4-e1ybEgBmnqyAP
Tt)~dxJfBqtz_76wBM6s(}`cT#i~zEge0jv^-NozAM7|d1cq%o(lC#{rZA5o`QAI$GpZ-;>+4trXYL9Gur~(;w{|bxw-NGTXbY;i
86HdZdH=C%|5EGouJas2V3O)wR`$xC)+w(UK_8r4Uc&@g&c+4n27A9kM6{+#W!c~WaICEsWNAe$Q`tgZY^>nSFrRMP^tjlx57QaS
K5chDZ2)_l!`78U#04<r6rdSPXX`XBkPo4sdRLsC0+%l;n^4<uy1bi=+j@ZD2MIwZzlgAOVU=-LaHhl3wP!#xu+H@biq1Yw8iw-n
^D6+g3srEUFpnMEgv^5bPKB#+!!-0$X(NKNo5sHQzTo%he#WiA5xT_8pTf`L1iyA@G#eVi#74)tvW&BC{d)A<Vb)!(yIgm%Y@#(O
Q_D8&+jMXHXSqN1eN8o+UO$s(JE-wmr_X!)yyy3oAcT)Itt+dUee_I{0jUIYX`sLp$73*qjwu98SY;_O_r#&EjOyEH)Hp!BBTzFb
*c@F7Zfu*>!D*JobHPEiWe3xg`xmU1S8%mBI-&aq(gi)RyCGLGVYCK^s1_!Rc~gIdFyEl&y3SL!2@NH4;&y2Rv&Y_#oYVUSc*D*5
V?WR1JkOo&p76h&W7W2&$OtZBgKTAYrg?|7ho$PLHQ>B#c{#>;9p?=etj`PWSUraMFnQ_QNhG7$zOQf{V-7=Wb><h3tL)3lhUVcI
(&19Y74PR1R*%p!t}1OJZC%<0>|O#<w=S*#=*pF|Fb^=B(CM)nJcH*)zPL;4D=pnfhz9u&Drj#ae-^QZ$D8qU>xNYvZUMOXuqgbh
aTUKmD`0rzLNwBny^Vn!DlyKlR9<O%<w=#fU$zO~;k{n>d>**p&74IF0s$>#?Uci@*ZW$p3t>WncAj9elW~F764G#>5$n%e=m!_R
&0$HPz70;X#Ucli!f<gpl+Mnw8&Vv4n4<}C**Hv*yVav-y$pu{kv-IC|7wQwYD@Ks>!WSjf_2^v;Pb=@1=EsnDeIo+m3^DwkhNK-
)a=zSuf9<U+fV(x-;RYz{S6QJzPQVOB6QxjR1x&;9Bn;WHn#Kq?1u`)U08y?&D*|Q=h3>-v5VtD{58v5S90#e@#%eu$F1<CwhnXL
1A(oZ9;L?lldy#4oaQ+ozFl+NN?a$F5G^Z?f!RhgOd(t6&+N{_8YA2?GnD24ubMZRS21mJI#dF|c9I9rK&GV{MueYB2!*W#(rVM9
@+N=@#}$wSenWeb*dO3|j*17y*^IMgkK)R)N{M{dc~j5dZGXC9?fwNZEh5b-vzU`b)cdk5Q-R)$5`lK;1<X$#dwi000o@o~F8FLy
kDxaM)%Mir(SEbv{|Wjawd*`W!^4Gt+iwgmh9QrL7NJWD^Ij^;ZJr|By_SPXUo0~}muIi4o@`rPpkTm_+DuAfp2N^e{JBKR$??k4
a7oJ^RiG`-HM>)RwhZiSpL)k)<TvZB8l%?l>fDJq@tt$V2biYmN%`QC^0FNXq{2mtyNrrC9JXs?D#T<}aT;!F?n4bN!8gy_gs=#n
5~1|_-rp_3ukF=7oBrE*f_2Ne*Vd5mub2JPotM1~*+Z30M?o-r{mWXu%v)P=EfpQhjJ_!Bb}?7nLU~$B&71_Zz&yIL+OnClsd<;b
Fd2%jdKl7N6Gs>G)&pF7C7>Hr*<{&7+2tSFkK<SA@?dSRT-8KqAmg~nnP?jvi&_>5W&U8EJT6@OHrAPg{<M4zPUY;^CG9j_d0WP1
4kbBothcg-Y%kqb1GJW!)z8XkV{I$WaLjTZhT+=+0=G&U>ok!_WKmngXRnE86m{8J$DXYu+^D!q_mYm18*tImn&Os6)>Tbx6x@&>
Ap~;9Zzm-#z=K*eU)Bp@nE(sZ$<+P;1wR^x-#}hnzbkd$G^!nP9nmG^neBUAXL?LfYu~Q2T)tco)+TXw#q7EQYPkoZp)0)rCMUDg
Q*Wn!n8UcFY0Zd|&WnAbTFO&fh`!dg9L)~x_pzP7fQMzSV*5_c<u8qMJC?2WQ>Dq{KJWa+`e2&3Jn`1!z*ENS+`Frw;hNTMTsIFH
v#fAEM1|g40$W8royQn_v}(7S>Jn>PJ6SfjthTPE?t0#cx|`(yEOFXp$B6?VoYwupu<m|6{I+wX*;ed2x-Ht(<Gvf$e7<46^PC25
MjBBILZq^<T(TLXVeeG1NVfTp;sr$n`CdT==Fj{!TX+UZEKkkp`ZU2V6_)Sm^Y)<CgA{~yb4m}EOw<%P3=|<cq(df=)-hJNMF>Za
YsHx^5NTs?V*>|G4TxcUtD0oTo9H=;sL3r*JGee7J1E<xtC`>pM9D~3*eXU_zhYp065ft&r<Jp|Ow)U3;~;Lr&g(lZcc|A;<ZMMF
)oXgtchew>f0gi>xa@+5uZ$=AE)%cJo|1OP*MvJN)ni_cdA~rE`MTEk`)CUqZLh7->^lE%nM+Jw+Mm>vXP&}uA_{Lz)-JJk)_kv-
eJ0snuQeTNT{Jfq{nn?%x8Ux5`lJ1~2Kcv$%+p8apHlOG)dRQOyKO5C^S%?uQCjbV`P`;`8Mm49ine6dpck)~LDyc-ecZ<P8)QHz
G7P4JvD%lZPGQ1L-oq}v#BU=J*d_1XQVT@I=e}U%pRVkCi=?)vn|~r<U~Sp87NR+fC5~-i5HXMVCs^Sz^Pz9E@rWsKI2ka70sKMe
hYQm5B6u}SekgQ&Z9q#y=-EVd_*aGFz{2g`v&?2>&9y*yV4=I&$w&{f&9@4}K)dnnfL%XN3t6z}I>4)!&_dgk5c)A29G3g8%R7@-
C&H!Kh~@;lMygjPi`sE`O#^vV!gGA_1c<L3UfFj!blJ<vtBD(^a&iu8X)njsS^zP>Zhz`k|Anogo!rm)W8&5?PBue$R;pW7V`=R~
7JQa=T%Kg<rv=A-E!P)o!}j3jac|gu|LJ*IeIDKoJiphISPsZ(j?kDYtH^TP$FN7YuraGz2Xh3y4|;{s_kJ7eHA5_|6{5u=E`t|m
=J|k-A5m8K$fd~L)(GR<CgrgK;Qq|1gg=7id4}5sj-4tX3Fl1X+)odqSWq>vg)Zm%28LS0(3<M@q3>JUGalQCi>#qQBnS=f9*%Js
9-Hvm-hC^Ko_c>j3@oy31x4m>zp&-j8`o>scM`FK(ydz-cl#6@P;fu=cqT-Ycb(p~;Fiagg{TCtx>k`5Pt<yBZuio770D}vL4MVK
v;AsK)f$oa(!1K5+2P)laEP!}1swCue1&d`1W1(t-=(2T{VRc!7OxajuW`3Pc|ww%>wdyxt_N^(qm8(Jk5@f`yIyy_e{ucy;e8=g
|HI6UwhIwDQ0@!nv7Em+t{K?R^58gUf^4bVS+}dM*9<J*Q5kc6mvW_Yjnf(CE0)XU)26czyA6l+hjY8LyK_h1A47k7172-?zx%%0
dg8jtDf`Uq<p3YYM&T^zp``+18|=K)%u16T_Oh%q$F6b8W`J+vbx)i>W!urUX9lq7nYTDt(3SXWRq7hpyP+i{@J#FHoLPS@kMseH
_xU8tX$@XR@Pv>1{_h8PZk;sd3yq^y&UF%>K|U*5;8l-^53XmgoS=k{GpBpbS1mtml(}#mJqxl&DCg(K$5;DK^~N{qr$@ln)6~nR
T@8!uR}I)|%xvt^n+0wW8f=gSC&P;_63+1#d4QvAUeeOy<%Z<C<Y31voIQfJJ*Q)00X&;k5jfA+#L7|@FcZ)Dd`}g)cwFCQxu*x~
nbsq2XWY+lH0*~5w(~(;j!<{c<Kejwa)#*$`3Pwb>4?Nh<kJJ?4(08qtDi0hmDz-*PL~a*wVUiW>37^{CY-&$eSh{KnAw~?`T<zY
a*eEd5FG>x2Xps2diTuZgOuXRQm<09lv}Mw4UWqc=hm~X8IvLTp^cs5L^0;tfiR?i{##>u7-3p3Ber8xnkxs?`VF8kpHpolE}{N;
sQz9C4gL%BO)zziz_~WCOkCWM>h+W%X~RW)gsDos6x*D4iX`MHjh*w|NUCYPN;>E1b8;g0>jhp7wvW(+cN;{~cr}ApCmc10V9Bt_
xJtjsxLH$_%tB@*l4OHF#EAvwzBine7<9F6?cL%`wIH6Et$qNtpG}u+gZlzxONO&Hq5mgmmoV(fAK4#iyr%IkIL0f7Gy5|Ip2T>D
@rpod7*7wBbErq(WVKy)y>4uKxb12`^>#viYpCz_>g(z1*>lzQboqb@>hn3k3QhNru6{fnm&p!9!X_aEJZ;_;Fdce4v|FX!6yQ%C
FFRfiymDvItJ8~9i__bHBV+>{C9D(NT?oTGXJ-{F#bn1px2m(;t$Q6C;=uqJzs#;M_vFc4x1*;EgGCxzFOi2H4`f^Yd@@2sYqloZ
hF{x7ZpCI_wA8C_5o0TV6~B<;KX_71pA}W{&+mn^WAz%>+hv1l;tGrcyB>ns*Ru#Obs9&Ac1{c|`O4#&(>{S$XByM1Go2x?mOS52
>;AdkX}&@MuT+*SKgcgRb!rxJl7fuVuLs$@vTb@EM~ldD*eq)#Rt<#R`OU$B>RCho15mc$4~X=j`!|w(jU=APPL<wN@7B<7!5=Xk
;LjM25YHi!0OY_(0>F~Mp7iVOz@P18FU^yX*Qu_9C&wxGQ>}+$cn9Ni7*J*0R9Gc2ZaTK}xQPfu#1j=)zJS5-p}B{NJL^#WriR`4
z3p6Hu0O0?+K?f9v|{Aanw2j@w|KKg$RlOBI|5gjnD`{0z2c|p8TRTrre*f)JTPS~XwN+tJ^TtD_QHDB(3N}^(;E%C$B#ZKSFK<C
gRd#<{>7zlW$YiGSGGcHj>!GK_?MG^c<Ld$?+JHvh_<04G<Ze!{_^U@b$IS4=9HMNou^|QcK`w4dGxO5v{2)1Ki14evwwIMX|LKY
v36DISxN#7F)&lF=^>S)jAxL@WrwaHc+~962KoVouQ#w=tA!xJ5x2Hkdd5u^ueY*rL5#*Kw*kYjV54Pj#|Vx!AiA8anq9Mj7F^1w
o^P|f&HC2ct#;s2$0e^zflK$H?p?hP^=>@@u1j2Z`zO5Yl-nuSQ!a;CPFW8?tT$Y|Du)D?+mzF!jiid;+hP0$I!U_-yJ@{Be0)`L
RI+LTETEH7tHpU&O;>GK8@1}7>fmNSttpL&-1R)#H0Z%dP9;|&IDPGNNiL5tP;hn%HVy8mtz5wiS-K&qey{A)!0+Gr#?SirA6tml
z52oHe<5H0;TwGO(;<QbO*tK~jjn37k@DHmZVf=c#;U!C$7<07>V`J%L$|4*ZM_sBDM#IhR72bg%Uz|^OtU1f;Nr^#(TXU3p6{_h
u7X!`>{J$ZF?KU%)smHdikOv}HO#)MPJ$%0?|8(y!7bcP>Xqdy(YVP;>)E)Kh4gMS{catcX$4zozHIGPfycxVX6o0J!8taM`N9!`
KkN2;lqyn}Zdh>Xxp;ZL^?l3tE#6o6KD(b&zIXZF)V--|)8~fEC$C-HhrIDme5JhK@_K)d#|@5k^CsqlE9k5dnuTALEgk-fT@>we
Y2`o#A4GInD3FRb3)!VAz6}jt$%kNEKz>e)VX))wpZdP1ZSL!6vezRll9g66edXMyTKYViIJ8AkR%1zKt>`9|sGgv<dyf5J$B#d5
{fAeb{3F$?`;w~b8vaYL?%!xH5Y1|RY1SYC?k`eP(RO`l_UNm2BxtgJQyr9j{X!a#fHnG*Jmlh1riso}bApZ=Voeiyg^*~T5eb1;
2Y5AfVt94oC6myTG&6NO!Xo;MT|<hDhY7nLHf>jhn_4d#U$`iW?lP+`$u0@;N3crBqDZQF02;d-po$?Tjiads)HUtJATUfNfIqDZ
j!I8Lv+|Is3VxQ6Q@F)cx@D2as?I9!MZF1}nD=7uMc*th5@!|XDqzsIL(p~|v|aNdrbDE&8xL*)m0JS&#4`<-94{G8xI#JX0>^kk
V&O!DQwE;XO9I1=mqB_p+&1oZf2a4IkJYb}E74|eMiwAR7HO_&tA0wX2ZRS~m88!W@Ke0N6?TqfXi=PMJI>uVk?-HU`f}q-u>Th#
{XO~R+xJJBH~iWznyhBEev7&rzBD73bl2F`(F(PPja|=30GcmOAMvK=6oYl!?7)pE=C$K9_^@OKiJW{omm3^I%;d9hZ7#R(UZE4P
T@x;`#>I8e@H-VqI%Eb;l@1QOHC3>RZxRB+EH^RMd?GAZmm4O{EumuC-Vn|~LOz6Vh4q6`YLK#shf8*50a(k=>df@gxgm95v^-NY
ws9&+jHxTRtGQbzvF2`1;>s;eZf2*NyQp&_jv^2CkyFQv6S=Qq-^G54^%Bd~t+!a-V!pvKG2Nh+@OwAxT{uNJ{vhKiAA+@s1+Y=D
<g6xAi;#<ii7UtW{#lslGC8<Hrf3Xm?B$?e%mG~DNM!|k_3b~yuB7f+D`@KmZ374KzDCI30<<Q6L{nM+l1#D@M*e>osMo*HA^JxM
(eU+#T=#$Mm6ZP@w_eX?cPIaGi@!?#zhKJ`VfzGUm{Z4o5UlL#xRvPFobEbt6ga|q*sFk;JE^_{uR0dfhz`_h>=H>dm-Lts*s<5Z
P*EcuFBbwL{YaF4QI_tq&1WqFMvUxg>I){zET*|sP*Ev{1EP_(Stq!m!huP?3ST<kdIPYSyD}3YEh1G3<SM5s3rmi~Jc&9<U<I;h
==Rv1z}VeMyt8~y@}3mfbyrw3eOG;fU`1T3JP&a+UahxW-)g?(M0+L2ll+NaM$u&TTxw7b_L*RWs23{FZW7(pb-Ck7LA)%&(!&*A
$4Gk>=nA8QxPr=h)yZFb&d~(UaDD6*7rI@O?$3X;RP>H;jR^cL1#`0=+FQ*IqtryIUDZYy(aaIg|A%1zA=Tpqf6+Q3wct_w;;#_n
n=JSjOg?=6N-r|JnJ>0M;X(w(yzyh7GRx2h`(nkg!+kQ2VK39Wwdm(UQ7U)Hmrs7g2N4`JK6Ksi5)b@K#17I6&QXk_YfQs8sS7iq
5I`k(gdNn9<KBjLbFo5%U3v~05uq(y;9)qlC;cP<)#R&;i%d*L5a7(bs(DehN?;*GEn+DWSPS{HO>!@QIKhn~uUWAjJ&lqib1F+~
uT`H_!8+}WUh&%&Iky7JRzunLjdvIpmD;=I>f9puW>&a+;nuFP2y`MC74GsoMx_e7O4}A6%mUrTLPy>s3m!re7%0+yHphE{#9CRY
sm6g7M@%)BuX*a3d{v<86|<p0r@tjlu1o1w58td<>oN*^)kF@hiV3!Cd0lfYfek+gaFSu>pXmP9Qv6@>Pg-efwZ%4WqD^0Umbf77
9Bhndqx#7CWid@-<_ut>ji$?GejcU=d5)<t@i194DC0PW)VbCtf^Bd(UnBS>gf+xv2-OYM_SN)hHhq?=c|cpVE5;RVU~|S74OgTQ
gEi~Gw8xqyyi%Bg3&e$bX5q~$R4Q$F%;|*3?8f~y?%jjDw=|PQl(_?KD*P8+m{`URSmSGpaA)0_1=w;<<PWQ`XD~-XLA_V`Ss~Q*
vFd$Q+osFR<brk6>#CN`O!(8Y3`Moh5vpfus&o~!QHb~gbrG0AgY(L;sPN0MJfMd`aA8*jvmlQG9Qi{cxfMa8b_=_f^gEcQ{H}&C
{rGxTXv1Y!ZD&27@%=OJ%kWe@Jv}<WD@1~yyWsgb>ExO2;#vZMZflYaE$vEw7bm|$S_u%yMz`$qd9F+mS<5!3%7jQ4K?v}(ZSc8g
DcyXR;u|=8pl^v0o=rc70O`}SOf~ul^O3@sL(0Ex`#4+iK}hVGK*TnAG2|hn!6!G2u8+@#v>P&WlFBi!N8JF9<Sgqlu`B!(3*K5=
F5zOyBL-JoniYNxLAS=`VD|bWc<|+qP1t1RAdP6aULw6fKcc87hLQ=KR5~fmI(b?HPkTj^<(Ypc#tApC*s_4nI)G8^N$!(`oq2Cf
a@SVQUjcb8f?8-3+t#gnx9oz^+|ER*k-2*+tjf2gGgv=>Q{^B9aU&2$WoUjFB}-OR!nBA0iV+G>Rm8U1tcF-LQI%aZyWYU%weYZk
+7CwnmZ~kk%XomLB$)dpUXPfUxvT1Y=j$BHC`12ZzoXW*&l$w9h{t0qx%~1<wSZ7OYu)l$mi(88YCcO^6{dK7&iDI#w}v*%K3bl1
@cd*_#eutrB+tNRjNei~(5CUEO}Ux>F+0uj)L&cFChlZJa19*2^F=IkLydEdwT55#$~^3_Y;grxp6ofiV)mu@sRVW?Pu%p*t)n5E
bg{t~Ygc3(Rh~^f`sv9++L)2F9JcP3$$z`^oH}VBx4P6xYNW6Hc8jyKwKQ=CH?OS}{D3Ngg1nisQuHxv*dLgk&#6AQexHiH-L@9f
fl&q432~fU!KF5FxWK;A&~@oR5Qn%-44Xofs;O$aN2<Nz3vcEXUN29(+Qo)|z!tL2SwyBug6cXem1X-U+TO>TBj}J**Q6tUr+S_g
lW2=qq?V~oSXK!$6;BOsPJ2by2|bB>s<oL&9i>7LX&F90buFzpg1n+khDVx`{~%0CI(o?_x9r!U#1qv2EgXGSP4`_JSDo>C-pbF<
`{(CkhWT}Tj{V+XCGaQ8oWPthH~$68!|vC)u1v>WU`fupoy&Hw`+Gb7FW4LY9<C>`obP(x^KqB+&gYqrBkjzO4#&w7k!^P%LfK4S
%~(yCjnBFtl^bO1+T0plKGCO<9SgT}pQk>K+Ocn>%#)jnDYITy&Rf|IyX>mA#J9ZaSan}$wG6j)1Xp;P$&$HM7LF3y46>gWZj@~U
NOZXF^rRedIwEv}@2le2<>xkF*Lzir<3@2udHL=LVvVAXqGsyzxiXoq?6R#7AR>FYO~7>ELc;~OUrrYB&wXQ!=Bxt*p?rXI@D1+)
#1l;=%CY^_NH)Su^{a7<221fzuyTA2KGDqEVLWWyOyFKT4Wnah0>3Zp?@9>e!PpJOrDY76TYa^%suXsKx#c}8V&JVH*YBgQGbdO+
>!Pi{B&emihtd`T{&@9`0nN)!2FTlZy*Y}gZOr8}k6ZNB`!e`x@c9`&Jp?xViQ^K}mhzr5m&Dn5mHnbG_KTi@s~ubK=!OZHkKB;v
J<Z!V!>q1s62rpwGNjp!9A(=uyD%XP)Na&JSFp3c3vDbm(=X#XI|w(l&e7TjJ$TM#hsk3HmZ;<8(qyM%r`aS3=EEJQ<-GeH92F+L
+R_%Y9dH#uCo*axe`qlVgp-0@6TA?Q{%3UAfp0n+kqwUEB)C2nH5FNBwG_2xd1iGdKwb#qW^+yY7}XZ_n$$dsIf=Q*RJy#-{q?x4
T-Orx$dSJvlCK#kf*gzZR|TGcJg}vvnzkJPD<owVkldh+h7R8u=yAEAJTb3o=2y4nIB-(HtKudyboU5^IWp7IrNYmGVEFh_vhWo*
-SqRr_TB4JIpY$_rhV<-5UmX+0mtrrP64qWw|}1<WFd45;eK~t{>o&;O9dEw!x#Yp@?!3H`8lWe60c<UAlF`VOBVjYI$Y~)UBkmf
qS!Cy1{Qe&j+j`BZZlyBW0EmrLo{tJuC`vgLHAzwQR6i_!J~0!O6fM)=PBy%1O#EPS#ddWEG_E=CKH1hbjV<fgM%BZj!;A+hiQgU
r(~wdz-{G8PIHUynZRqxX48V>kQX;C!?MSDALhg7-9{+eiRD(Uc$8nbNU(;Ii=}NXOJ=RxLVA})$8u-!lxGcNmt(ht?i%HL(s$8Z
eS+wUk``=~CyxqtY#ZeYH$BN%L@2_yP_98Vz}wQu!1=<vfhSEAX*emkHZX?`Ah=B<-PSburgaq}ce*i3Hj1i|bOn(dY%*utYmbWy
vsS3q8kZm=yJq(~@CtVpuF7(h_xo>*%l-4dZqDCXYMF9kr^cc6Ti#i#I;D|Q2HFaPYweCXNtK<F<u7=>lpEQ503j#z8zQ5)^w-bw
^Rxc!=~MbE+G8*)H~ih)+T6{qZ@|e=d%!Qm@C6H0p69=q`+n|+(lGTyvwME*ee6SgM1CI;A3&uC#Cmu~tsq)R+Eu(s#ggXH#ko)G
Fs=iP5yFDt+Tbu#s!5AZD_o|HGuX)yhdwH(tO)TLJ7CPbj_h@`va0F0;&u%C>DPn()PN^>d|Kfs)pnZoG-XHJ&4mbA+R7&`3g=C7
r7P`b-0}GpSJ4Ys6miw;_`;u?gWOzq*w+=ryBNr@_tJg#roM{4yf|F9yVvYRhLVW_(O=rQJj-Q`mGe_MLiN9Jjc-JI*l*py@tNR~
pq^h;(`oRGj7kzd;OXjRTF$#-YQ$wHRz_+|QYl0P3irzhHVO#HVeR7*mc6cPxtNQ%QCBm)e_?OQ)^qabJbsSj-q}Hyt-qh1%oEe2
r?F&?xtPKLswLZx#(Cp{vZFAe1Mf!1KZ=`$L5FsesUX#R{W<H;67I>JqdmOYdl1aB`GrBe@-<B)o9pWr?t4Nm^@aFjlm~uEH2@$|
Wb_Au`JQPzj9n3Hf>*D$Nv(~;t2odcmL<<aEQlAzUgv0Q>1%b%(z8^4X6x=4wD)wJHYyv0i$E8$0%Czpvp#q0>3x#ZYD1BEv%ZK}
Rj4w|GR{yz8jRWw&3qMZn#kp(Dl4l>h}T#Mr~;R*9%!~Do!flV#ZuL@E~0Vh=0WVBP>`QR{haD&m(=rPcMsxn;&$?Ias|P>fa}~5
T`qDxRB0PDKsm+SP%k+H+@_In>z>V;@#rEU;(@SEhF$b)XKM$qiU5|g#yOH4@*B4jeJ*S`ZaQ`+T#T6z>cWmOHi3P!MaN}$|1em)
S(b9|ZJtpI!+jm+wycHCwaz+Ubw0`jJ+s8v!uDsBaSDCzZL)@7ivZ335--_*`{XEG3$}1&KQAgtSa>!`iL>3<j%NOx`Mvu0WZy~O
qdueAgWd+S_2x-js{c5_2ag}@r-tlYc0Jgf9P<f*=v-(Rp3d~}dB(vXn%;v<FAf*O6N8V_IBfxDDwKfmlLefv&i#s55wfg+R3Rk`
<ZR1i>pbWv4TMnahFOQE_{-sK?B)aSK$N{_S4U2Ef5yE(^x%S3TARIEC3)3SR$6L-IFIhw#ky-y%TABSkqo%Tw#3?^Hn>Y!nxq*e
l#*@9r;8VRl)xD|i}O9fWT`WAr-tXi%x7*0{z>kOT47sGxm<F+<aR3@E2%|HmrPtq;}H>M+`D!ZT(;f1etm&gy1-X9CEr>}hMD2X
wBqaTdbr&c3WKAg9m}s7T~gN#uRf^jTA{4q0pG_qXO2O6xAv03nza@-`>lxU<Fzd{kIDBnXAea*a^BhiTajyk7Pb+NNGY#%FeXUJ
iA!*W#@Rj^KUojK1hJRIFbNisuWH(c^@#VKKUexW#-BBOYC{>`xxbTx9a|g05D+&F_NS>V7?rFWVGi+!tqTo!SN)St*fPKb8O2RN
fD7z!gPbkq5rF2hB1GV%iyrrgor9i}hVPqa`v|AHm~HF#9R%wuOxnbna_}my>;aRHcHH|OesCd|Vug*;o*nd{W<f3O+C2_l#YN>+
wKZ)P`)<2{$=XiI<3X#HR~Z)RS}=vU9;yZs3qtEPb}vL~5s?~n3pcN!a~${nWFEw9IoEYF9VGo##5Kb|s?R2WZuLI(wQ7ibShl%;
l^`;HWa2DZj-yQ?WtoctTBl4gRvFt0Kg*yO5t)1?!^$<==~NN!vI5dCh&{Q8mu9(NLyN05vu8J^Z;c4B`Q<=*scDTTM_VrU$?1yc
T8?F68=3cUEmI!s5Btfl?BYI8Z<wzspX;)5mRMZtY#}zsF~t#1<mqsxR4;^+Y7pcVr@~9^5jqyGarcpb(N3F5c;~H5Hg9TV)uWqN
f8XVEmd~EvOSs@4lRcw_?IN$NDG!~D{nO{8f!a18@j#PASJ#??7^!+?;EP9u0*<aZaHmpA3p3@%luDT@v+Vr{&pr04PG(&VV!Cz1
k-M(ft?suyc3ZM2*`^4UW}&wo!wJM(7I9D`6`TUdEfb_((mtDk(0$hUZfz2{o&AIhC&&5O#d}ITpIT3aXC{zs*A=b`R%_FK;hu7f
(^Uian&F0M#Fz^qG=67hgXc6hYW3Y76s>)AZ^nu0EaJVY&k6yi?nyz?!=N3oZxHrgti4!V%aAg!8PKm{fo^gvAsTyj7tcxMtV8PZ
4F2o$t(ov}>D1nQ-TD4mX-bpDI0b}+%Hj#0Tx=?KKW3V#pX=v7Si7;!?~NTnaKdunV?9dR#;~Wjr?KKPAk?xJu^<FYeipRbq9x8p
NZy!I8~NL&8;zmmyu(&nGg|HORH^WNkg}>RDw190(0PR^(@@3u^6Tb*el}+Quj4WKHBgqbH2_^6{2knF1F7WzD7nZ2YX*H(<(zx~
TLq&9ubA0qV91bsQrnkQ?28rR)CR=yeGVhb<Oj9j`+u9`!VSnYr2C`ZZzfpoRgLZybr+55!O5;eyk;kD5egN>mL7|H7QbS$Lr@-X
W#9yJcKnHKMCB(oKF-xl)lSvqS&v1IZ5t&NHB1UVlx-Z7F!A*?<bb(|EA1P6%~)H}=Vsz&2QCeDu8N+qo(x&|Q3U97)|PeE3t%I8
<mm-8{2j$7$<HKzs{Gm2&!K-nHc0)ML&|<;{h1Vz<!2P{(A}YXkBlylMn7N~<v#0U(+33M1(hx#1(#MzSXNd)Ls&v*vbSkQbSC}N
qom+p!~3(p!6;g%lL6qh-z!8^s@|2}?lBx`TvJ@eP-9reaY^IchH`n>2lj9g`qj`0BU-i`H{04#BT9rz8cZ7qh8QdkE{*gu%j%|C
=b4f<b5j-Hwn?)_JhdO0!(~1jBt3_8m%NT+^|20d9>P5M0twTHKTLg`ICh@%%AEC(a`?-JyEJJSrr;+J?+b-3DAK(Tty4ou_<!;W
0i!OX_}un9<aw&&kk{Uwn>ec6GGca3=Qx-;vVUYrU=&w7aRj>{BrKvr1P>!=Z5)iD?AxLSZohGIxNSkFvf#s-TtF=bjJ&~dQ_t`t
sw_5F&Nm-MHbI^cb=GFYK&m25?0|lPX6PP+K=Z!IysP=dEeYbm+Os?FR8&fGj9qRVn;k3?2SuGuTzv=5fL-q*?nU0KdT;K%4tus|
9=OP3<T1!k(m&u>>E8AAvmwS5z`cW1YTaakPpNE#Un=B*8fnUuA5}>Bu-sYY=IS7ap@WrMw|Kvo4=aE7d#gvCu6=EtRa$$fYrmEm
T$+Y{8RH6LHO9g^J`eu^-QGBs>Nu7V)8GRqR&u9VKZR9oNvM^?aF2((KrgPGdab5juTV|JZId~wJyz&9vv5$jUU&ENS;?ywD$;V!
)1K2B$0dx5C&A{1I*fHlGm*=XGi)cqLD&dp>-8{WuvCGKS>_%Ao8dY-NEPGA*@I&SsW`U_Kj7q6)O(lL^5Ui&li$QuyR!<46Q)_3
b2mGjW7U90$OB|;vgWE;&@g1WSN(v?YH-&~*)A30-_Av^i>Z^Evnol=lPVB41>#EAO>HNRasfj&h$}cjJs;50nwh|dtUD77z_EFC
Bge3`5g8CIEwKs#0vs#2$I76i1^WjG2{R}lpVHXXQLa(0h#3(QdU-{7LwnEtJwsafdmgvYLsW3R_9aTkmdhL1<>ftb=lb4obE$Ka
D_aVw6`G&P54=qKV)ts-d00!o&BG3q9yrQy&i<_aT>SgY_gPx|$DM_}wVWx!?<~=CF82H#0(fs52lTYT3J1Gf6b^yPX<@Y>X;wTN
Nf68sNI5{s2M!*8QnWZTvmY$WNxg-mKv<`*VBgUIcf?&|_iXlJ_G*qTkky|z`v@KNvzB|FjtoaUl3H<O>k7a>9D`BKbHg;`$b!WY
yn>w5aMYAlxvi-Oq21#F5pYb+WygV)X9Mfe%rUup61Y`=iu?ez`&l~Pvs-uX;^3~XSP)-89ZhZHI3b$WDk?QdlFBIrn)qO2w$%JZ
F9i-%A3$M()75YmeN1XEirFj`0h-ts9OcS9I(-~=UF1B2b#mL)w#%adzWCbZxoNy+ts3N<vQ99PQHH3X!<Shui^AJmcV;hatJxNF
t%fNvmBTTApey!xE#tl9yXI~5#p;&J!@Z;M;to$~!<(k=wR`=uMaJgKK&<^|8-9-P*$Mof2Aqt<*0ATFW8!F=HJu9wAFu3^$x)%_
H!E^_PYF6|ZPp3c(zxe__T&=b3TdX+l(w8VQfr(eNEKijSh)<V<v4Am4UJ5RStyy+?RW|MZ3MW*pb*@-JGwjQcXXfV?{Rof{tdRz
{ys``f+w4D?3^fibGs+)<G96f4b5tOkrof+My&}ZYh*oi(q?!;v_D<@h(STr_XzlyKEsiO?5{k+Q1Qt=MCXp!f1>#WXbka2z)qPV
K2O?P3(}7yT2iG3H*}Di9f+0ag=+QF24>nR&{^A-#;9J-uu&?9YdAf6m4hykV>s&Q*6h|~w`8tt-o?IWjqvT7#LblfeP(@ReNNEZ
_L|K(>AS+t*!SXiiP!#yGOztz+?DOk+rfQG|DJn1`CfW>w-0ViXd4h?3m-6KiPs$W%xhN$gcO`#>t3CGy>J}5rx~~4t{_M4a09Sf
dnA9?_*qB%IF6q!F^t+qDBkxP?;75S)|c_UWe{m$MLZ{VmC-L{Wb^T9Y*U`~U`_HvO(P7{GYo~pQ=Z8wtoEI+l8y|E5whjF;Mmmi
XkDvo4wEOTh!97Pud%Hr5JA3fMWyb^g3-^^te1cfdB^bf?)H|GU;6$UaB<x}$Is{ZZcLvKucn7rtz;%`F+J2;15UoYV#gjo%>xL-
Dn`?Xmb>nR@e*&=XU8qa%m&FE5<dF2Txxu3-NSNpVeN;@*-Ohy5qBH)e*Zo^lsdJ(j6JQp9PSJS9obnS2kp{;=*6~`GCbMzB|o!!
%5Gb-zv*pz$gBv?O=BH*kE>8wfy%}hN3tNvmFx|S2!72O^*Mrd;LmW+{wn^+{h7fZ-hJ<Bz`x$3`{d!B`aAWX$$w`5EY9Es_>p@W
@Z=d0TZoZc%3#sUyk7bje;Jg99OF<n`|MjXOYsFie+K^^!zX+Eo}W4XR3HExE(Ru-;mX705b$?Tfs1do=P)AA=<mNqLO6A}7kih2
XAg}rY$cx+vEllz^<DCv)1C8`GCN5PKKZ~xW-eZ9_HDtJ*Ak^Xv@u87wy`&@Ta{|#4I9VIQ`tT$x0?QT?%lih;Lc&#hkk?AI=O)M
LF@oZAM4LLzbkk(T~k8r@Kj^LYHf{FTga<_Fp*lr#Ae<@h9MHH5VYV`=NOV%7VhH)YNMR!{=lo`hROOF5ddu0<oa{yZ!p~2+gP^E
*P4SS4PY)~ZkETnRh!fG;>oVZhiQ|ao-SS5Ti7ns_9I~(xu)V3#Jmm41#WEj0SdqYJv^p2eqc3I8yKXsH*+vl(Z$k;CHv0qGxhJu
;qrkYTQo<sckVyMf6Bmr0>>JouF>%v1e==8#|vgq3s)cXgCpp#0KYJBtN^F|n#I}0T9#iZCQOx<8pa(wp{6GtMm~E=+$vn8x_Cor
ely;_gZqHPcpIsIkF*IK=ft1op7tPxYFuI`VXYxBJTyiKWy(t}-1Vz$6SU76-#FVbOIZ*GwnYYxI3Lpyd2wfWy&epVZSbl8?LZ};
L{1hm8~d%IU<JI@Uyd>Dujk62ITf$t)#LljcN@|E>_~!F?B{c?&tz><tK@6S`0ED&cI7?hJ>=cz%}*QmV2Ik6LTV*v18d=>6E;W}
!^q@}6jK@#S<k^uFm5ILc?zY_`q3Bvq@IJ72m4m$t@MXbAEV!(nKfU^X@lECAmR*d2w&R^MSLPGNhJrN;pT(vlNm;agmJXv*oR<a
WD9~eLBp`<a?n6axls%udl`et(M+7}XbxPp?C!4xqY8Zo2vKuIOCpW^XT)0_aPsCu%L|={JA3xt@OA@{vVUj)Qvv~NhKFMhntj6X
9{RTjhBrR7_wNv{emMIcC+{%=_ZZI5?sU2mdk+9ag5^v@d_M_x609CR{JQu~K71Sg8pFX+^?7apoobmlZLQ7=J6b{sxe4Z)%Qb?n
>T~8$`xM#2#hA>7fDu7ilg%Tj<vBTN!1c1de}e5+Lin3-&ipHwD<--t)hjl7v{9MexLaG80&t$IWIu0`>ivt~E$`oncu(`#<7eA`
*7dWjpSrYe1oh7KO7%?j7-wJ~nI5x@Ak37)#PR7P*FW)D%eNgFyO6Q*(>SlO09%~M(m0+moY9|y+l1UYc?oq3^%fGi0r~hx4VTW{
b@{bh5LWnR#(_PQD)W|!V@g-+|F#r%UYa3F;lX2q2cKXzSqP^_Z=czV14mFv2cJT+fv|9`X7+HA{T?{_`EvTSW-}&ruh_kk?5dKR
QI|7UZ*Ffc&mp{fZ*%t=UoQyqSt$<r9bi@5CxA|l)+T^F!)FZd6h71V&f}dT07?LNj&D3!(z}fB2~YYf4)^HqHh}d*C5&HU-oBB1
P@kYbqlMXg7wGdmH~Z2<0f9ClJaZV~_y(;8d_~p{oKyO3ihdn1U{i^43K7-|zU<X909;#kM8w5}fdOA?)C}ZX9dQ%PqP5rfPp02*
5sqSGdTxTP9PX($d`0-`rtz9Nm6g+@DrXR%)3lY+cDL*ASg3U=09)8C8K|vK9Z=?mmJvG74Qv+16K0B*FwG6^q@{!UHfeK6W1rZ*
)Q-V~puFd-8N;Tj5G1UMV7N3sWBbHY@TVvinQzlCeOz7KTsYl$T9&gPHn8Zy^i{jr^u-R@^qITiTx84rICAeAc0R)~&fK22(V9Wa
Hc*2@@hIQgbZOktiOrhWV6?CU1pE{o7PIg=kzd{X>J}kRr7jX)-AZ3dA5!fN+ZPar@-pge^=<Xr8Q7nX??JY6uvdVW>=`scrH>wD
d*^T`7&_Q1@Y$Y?u2=Jbpws0P$C~$Wi~7QG;PDy^cSj`y0o?=@gwTvHxF1+H-)h|Dx6=Iu!O6)obAf{JaArzzdi|^WErb7Nz_lOY
ylBNq<9HR@Eke1n<+U{3ljhgzt)3$H-|6-I6?hN*3wK|a1iqqI#Vy8Cr<Me#TH3YJBSZ?qInY$u<}vyP-r26*=nj{nwftZ=B6=13
54cdrW@=pgZoormYq-X?cxkP$_USp%wfe(vwV}}PpfB-<r)=oAET33iIBaCWrDDO;A;Tg4CBs{`{9nQJ+ozaj(~(JALn{5qk&Fh;
uy~y!C!6HbCIn2zO;G(>MQ3nR_vXoVR*hO**hOejUC(kB$=teC=v|sa=%dqnr%s`+hPTvjsp!6q`B?MT=A-S8wLcC=KJ#$~4jlx0
Thi?9^t(6jFG<wdo2wbO3tkT_Vu0M!(1C}&#Vh$T$I0e+0XTW|47eD14fK^Tr@LWw+9*Vn(tayl{sa7nTLy|tOZl&v5dXjb{ZFa<
w=?_yOzjfCeG_m6ZO2T>mSO!0q8r=ZS8ka;52Dl@xzQo$z=_658-c)~FM;!8G!XDIAvqi7Z_ZH1VSHY+xwLJVS}$zh8P~D<)niGC
m!!BS{%QM;o5ApTyf<MQqd+Y@3AY84G6tPT*Qx;BBKutqEbwjRbh`{2tFpK&JF8etD%?OAA+nreWq?4)#rd40(=d-ExtjE}*r}+Y
LeXn8LH3!JT?EHrbj!;%WA9p*ZMPy6HSUz=68h{&D&Xqy(46h$7Uu5syHkJobd7APLG$?0#9PS^A>LYCy1T4^<+-DM)6Ice&C?BJ
-K7~6-*C8AAI=;-M^Uo{kx_fE54>!I%7SAZeqioEOY+v8>@L8L0<BU+&O%oCl#FoOJhWo*R(vVi5tmQpmRaAjO`pLAteebjnoI6D
Y_UP7Hd5txa*t@CYxm0s`7N{K>t*8DYZ+f6Hed4v^Xm!!P=y24<Wr)@F+xH;zsGmqsX`-9SSsq;nheX4JJpE9y5+v>op6?8AI($h
3@(9S1FPj9&y9a#QKR`I7%kPyiY^Xn&bH33RyWTsXPc5q+Iq6u%r;DNn556rkJ5V`2Ib*Wo$^+~x%F@k-An(gPFpd%Lwbc@tV>kW
WXo(*F(E5Qk7@eJ_9F~+3o9d{Y^_IQCU*F6o3f{Lr*N0xk?8E%ne%0?&fcAC=x;FqZ{gmZ`9c61xI1-q5Q^$j>M)9~5DF^A6R|&{
FhulPXXg&Y>BbO<*1yu-oltAESLWj_$Co#i1sPAR<pIX^Egbj*^w<EScay93J%FqBGw>JUcsqN;Df7sAhz#ElcOx=#jtf3~-n|i|
D|@N_t^HetkBT_n(!V7>U5^ioPkl;zNV{}ul?Il4ed(<;e^?q;VOxPC$Fi61X*nQ&p<0@@N-b?4$B}vcillmxSMkfe2hGHBG%YPs
PwUj0UUd>y$bo@^BeejW^tgRG)hr>b9DYi&L|%zGntfq<OsOVj<&&~r@iO=7QIG~MRrLdWF$>_VYK=%B2}Jkrnr%&di@N`cz3~td
&i8WcRZQF-WEQ}pJq%Z3?M~0i7-b;?vT>xDVJ0miom2OhAagD`9K!AG+gm%k0jwEyaKZJNp4q-qJb!ecAJDV9z3ZzPCe1v_+V_he
n8iq)qdEMmO|RnsE8!p!FI-k@52F!Sfl+6#?(po7w8+%!cQbK!fZybh-wV-7@D-ZS*~#b%<L3S8hhrGHhBGwcIe29KV-aN|0)izJ
?{@Mr>hm~gIP1Q-Y!cgE+R*89W-+@Wv4s+(g^mXx{fRGu_0}-s{rymmHxya-oLsyO?Fo|(NW<xkom@My3qWo{EZk`5^6Qm=t}7hK
_|zV??j~)OxRK2OvCS3=aD^{TbY}QkCrMH@UcnOf-9swQMI)nN9%YxDUb5YHx2*jL>4U&EN-__AdVm$y_!-06$cI7?i~bra{aX`s
PlJHgBj9PtB%WOV#;&g8Jd8m>addqYLxC8xaf9NLZdX0?%2`=xH<tams%%we)9z6CqIy^=k_!LY>7`>fIxBB*OSaApxuXXeztiK)
)VaAETE1#aSydn~RUZoqbr1HMXSB?BQlC;Utyxqd7p)Hj1x=Y>U=&x$`ZKwE4(BxNBhLLb#UtTis%_838>_!^^yyH58yR|o_iSQK
m^rnDwR{Wlhg)=yUw%vRmXc`e(w9`H)Tc5qNBq=kIJKvsRaCaS4qN+{R$(>>P65Gb8-?smz)I^6Ak@!;PJTM^>AH8rrvWEd*BxEA
cduP^TSu&2w{#t6YIm~DWEZ&=7LRSd+Somb0L(xE0)>`&ELcy+svh@>hXXw(442H_EpuSz-t3rWJStkWC||IH5!R*6nS8cyx_?W_
MwQ1ReY@xUQ!erpxpn`>Q&HKbNa+r-1I(S*oXct_J>X8f4DLkOf82>Z(PnrNELg`wu+GBZFaN+a*eVU139+sk;MAN^yU0=zE~G`-
XSi%N%rt1N9zuY+P>B{ll9>Q&N68cX>_Rd_nRB76Et;7NbmE%-aOAKjzl4FE(!A$Fp<(AB<`^i`dXu$|7~NlkgQwRc*98o&5!eED
33&){b>i;CDa0WK9^&L`zzMGJ%%%=cg9@(SF0eNI5<D%HiIsPpTb1FGf{?2aEA0>PwMh6AH#~mVfwwo=E80l|pTr;PuIHa*LwgOL
IXeOdZGGOux4i^QOeR*bP=hrA#;JS17Kx;Ktd?zPCta|5DPt)<jAn>h4={Pkz%&h=$r_;r&R@Li)bnHi53(z?BL
"""
SRC = zlib.decompress(base64.b85decode("".join(DATA.split())))
CRATER = (0.2, 0.34)  # where embers come from, as a fraction of the image


def build(w, h):
    """Average the source into a w x h grid and tag lava and smoke cells."""
    cells = []
    for y in range(h):
        y0, y1 = y * SH // h, max(y * SH // h + 1, (y + 1) * SH // h)
        v = (y + 0.5) / h
        row = []
        for x in range(w):
            x0, x1 = x * SW // w, max(x * SW // w + 1, (x + 1) * SW // w)
            r = g = b = n = 0
            for sy in range(y0, y1):
                for sx in range(x0, x1):
                    i = (sy * SW + sx) * 3
                    r += SRC[i]; g += SRC[i + 1]; b += SRC[i + 2]; n += 1
            r, g, b = r // n, g // n, b // n
            u = (x + 0.5) / w
            lava = (r > 200 and r - g > 40 and b < 130 and v > 0.25 and u < 0.74) or \
                   (u < 0.57 and 0.35 < v < 0.62 and r > 140 and r - g > 70 and r - b > 30)
            d = 0.37 - v  # height above the crater: plume is a cone leaning right
            smoke = d > 0 and abs(u - (0.185 + d * 0.3)) < 0.04 + d * 0.35
            row.append((r, g, b, lava, smoke))
        cells.append(row)
    return cells


def glyph(r, g, b):
    return RAMP[min(len(RAMP) - 1, int((0.299 * r + 0.587 * g + 0.114 * b) / 256 * len(RAMP)))]


def step(embers):
    """Spawn and move the embers. Positions are fractions of the image."""
    for _ in range(random.randint(1, 4)):
        life = random.randint(25, 60)
        embers.append([CRATER[0] + random.uniform(-0.02, 0.02), CRATER[1],
                       random.uniform(-0.006, 0.008), random.uniform(-0.022, -0.008), life, life])
    for e in embers:
        e[0] += e[2]; e[1] += e[3]; e[3] += 0.0006; e[4] -= 1
    embers[:] = [e for e in embers if e[4] > 0 and 0 <= e[0] < 1 and 0 <= e[1] < 1]


def cell(r, g, b):
    """Character, bright foreground, dimmed background for one pixel colour."""
    return (glyph(r, g, b), (min(255, int(r * 1.3 + 50)), min(255, int(g * 1.3 + 50)), min(255, int(b * 1.3 + 50))),
            (int(r * 0.62), int(g * 0.62), int(b * 0.62)))


def frame(cells, t, embers):
    """One frame as rows of (char, fg, bg)."""
    h, w = len(cells), len(cells[0])
    out = []
    for y, row in enumerate(cells):
        line = []
        for x, (r, g, b, lava, smoke) in enumerate(row):
            if smoke:  # billow: borrow colour from a neighbour that drifts side to side
                k = round(1.6 * math.sin(t * 1.3 + y * 0.45) + math.sin(t * 0.7 + x * 0.3))
                r, g, b = row[min(w - 1, max(0, x + k))][:3]
            if lava:  # bright bands rolling downhill
                f = 0.65 + 0.55 * (0.5 + 0.5 * math.sin(y * 0.8 - x * 0.12 - t * 4))
                r, g, b = min(255, int(r * f)), min(255, int(g * f * f)), int(b * f)
            line.append(cell(r, g, b))
        out.append(line)
    for u, v, _, _, life, full in embers:
        x, y, a = int(u * w), int(v * h), life / full
        out[y][x] = ("*+:'."[min(4, int((1 - a) * 5))],
                     (255, int(80 + 170 * a), int(120 * a * a)), out[y][x][2])
    return out


def sgr(layer, rgb):
    """Colour escape code; layer 38 = foreground, 48 = background."""
    if TRUECOLOUR:
        return "\x1b[%d;2;%d;%d;%dm" % (layer, *rgb)
    r, g, b = (round(c / 255 * 5) for c in rgb)
    return "\x1b[%d;5;%dm" % (layer, 16 + 36 * r + 6 * g + b)


def draw(new, old, ox, oy):
    """Write only the cells that changed since the last frame."""
    buf, cur_fg, cur_bg = [], None, None
    for y, row in enumerate(new):
        last = -2
        for x, c in enumerate(row):
            if old and old[y][x] == c:
                continue
            ch, fg, bg = c
            if x != last + 1:
                buf.append(f"\x1b[{oy + y + 1};{ox + x + 1}H")
            if fg != cur_fg:
                buf.append(sgr(38, fg))
                cur_fg = fg
            if bg != cur_bg:
                buf.append(sgr(48, bg))
                cur_bg = bg
            buf.append(ch)
            last = x
    sys.stdout.write("".join(buf))
    sys.stdout.flush()


def main():
    os.system("")  # switches on escape codes in older Windows consoles
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l")  # alternate screen, hide cursor
    size, embers, start = None, [], time.time()
    try:
        while True:
            tick = time.time()
            cols, rows = shutil.get_terminal_size()
            if (cols, rows) != size:
                size = (cols, rows)
                w = max(2, min(cols, 2 * (rows - 1)))
                h = max(1, w // 2)
                cells, prev = build(w, h), None
                ox, oy = (cols - w) // 2, (rows - h) // 2
                out.write(sgr(48, (0, 0, 0)) + "\x1b[2J")  # black background
            step(embers)
            cur = frame(cells, tick - start, embers)
            draw(cur, prev, ox, oy)
            prev = cur
            time.sleep(max(0, 1 / FPS - (time.time() - tick)))
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\x1b[0m\x1b[?25h\x1b[?1049l")
        out.flush()


if __name__ == "__main__":
    main()
