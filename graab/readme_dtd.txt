Changes to dtd (and display-related comments)
These changes made to csl-pywork/v02/makotemplates/pywork/one.dtd

<pe>: [Person] new element. optional attribute n
<div n="TS">  new attribute [meaning?]
<div n="Pf">  new attribute [meaning?]
<div n="W">  new attribute [meaning?]

<chg> : [print change] attributes type, n, src. Children old,new
<old> : [old text] used with <chg> no attributes
<new> : [new text] used with <chg> no attributes
<gk>  : [Greek text]  no attributes.
        Note: formerly <lang n="greek">X</lang> now written as <gk>X</gk>
<heb> : [Hebrew text]  no attribute. 1 instance	
<lang> : [Name of language] 'n' attribute  value "German" (1 instance only)
        Make 'n' attribute optional  (previously required)
	When used with no attribute, display code should get tooltip
	from csl-pywork/v02/makotemplates/pywork/.../graab_input.txt
<info>  New attribute 'vn'
<ls>    New attribute 'ab'
