<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
  exclude-result-prefixes="office style text table draw fo xlink dc
			   meta number tei svg chart dr3d math form
			   script ooo ooow oooc dom xforms xs xsd xsi"
  office:version="1.0" version="2.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dom="http://www.w3.org/2001/xml-events"
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
  xmlns:math="http://www.w3.org/1998/Math/MathML"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:ooo="http://openoffice.org/2004/office"
  xmlns:oooc="http://openoffice.org/2004/calc"
  xmlns:ooow="http://openoffice.org/2004/writer"
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:xforms="http://www.w3.org/2002/xforms"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- auteurs titlePage-->
<xsl:template match="text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]" mode="titlePage">
	<byline style="txt_auteurs">
		<xsl:attribute name="n">
           	<xsl:number count="text:p" from="office:text"/>
       	</xsl:attribute>
       	<xsl:apply-templates/>
	</byline>
</xsl:template>

<xsl:template match="//text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]" mode="titlePage">
	<byline style="txt_collaborateurs">
		<xsl:attribute name="n">
           	<xsl:number count="text:p" from="office:text"/>
       	</xsl:attribute>
       	<xsl:apply-templates/>
	</byline>
</xsl:template>

<xsl:template match="//text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]"/>
    
<xsl:template match="//text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]"/>
		
<xsl:template match="//text:p[@text:style-name='adrattachement']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement']/@style:name]"/>
		
<!-- traitement des resumes et mots-clés -->
<xsl:template match="text:p[@text:style-name='admotscles']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name]" mode="front">
	<p style="txt_Motclef">
		<xsl:apply-templates/>
	</p>
</xsl:template>


<xsl:template match="text:p[@text:style-name='admotsclesital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotsclesital']/@style:name]" mode="front">
	<p style="txt_Motclef_italique">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='admotscles_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles_5f_inv']/@style:name]" mode="front">
	<p rend="rtl" style="txt_Motsclef_inv">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adresume']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume']/@style:name]" mode="front">
	<p style="txt_Resume">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adresumeital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresumeital']/@style:name]" mode="front">
	<p style="txt_Resume_italique" xml:lang="##">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adresume_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume_5f_inv']/@style:name]"  mode="front">
	<xsl:variable name="readOrder">
    	<xsl:choose>
      		<xsl:when test="//office:automatic-styles/style:style[@style:name='adresume_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'"><xsl:text>rtl</xsl:text></xsl:when>
      		<xsl:otherwise><xsl:text>ltr</xsl:text></xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<p style="txt_resume_inv" rend="{$readOrder}" xml:lang="##">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<!-- épigraphe, remerciements, dedicace -->
<xsl:template match="text:p[@text:style-name='adepigrapheF']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adepigrapheF']/@style:name]" mode="front">
	<epigraph>
		<quote 	style="txt_Epigraphe">
			<xsl:apply-templates/>
			</quote>
        <xsl:if test="following-sibling::text:p[1][@text:style-name='adsources']">
            <xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adsources']" mode="inQuote"/>
        </xsl:if>
	</epigraph>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adsources']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsources']/@style:name]" mode="inQuote">
	<bibl rend="block">
		<xsl:apply-templates/>
	</bibl>
</xsl:template>
    
<xsl:template match="text:p[@text:style-name='adsources']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsources']/@style:name]"/>
    
<xsl:template match="text:p[@text:style-name='adremerciements']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adremerciements']/@style:name]" mode="front">
	<p style="txt_remerciements">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='addedicace']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addedicace']/@style:name]" mode="front">
	<p style="txt_dedicace">
		<xsl:apply-templates/>
	</p>
</xsl:template>
	
<!-- NDL [R|A|T] -->    
<xsl:template match="text:p[starts-with(@text:style-name,'note_3a_')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'note_3a_')]/@style:name]" mode="front">
    <note>
        <xsl:attribute name="type">
            <xsl:value-of select="substring-after(@text:style-name,'note_3a_')"/>
        </xsl:attribute>
<!--
        <xsl:attribute name="style">
            <xsl:value-of select="replace(@text:style-name,'_3a_','_')"/>
        </xsl:attribute>
-->
        <p><xsl:apply-templates/></p>
    </note>
</xsl:template>
    
<!-- chapo -->    
<xsl:template match="text:p[@text:style-name='adchapo']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adchapo']/@style:name]" mode="front">
    <p style="txt_chapo">
        <xsl:apply-templates/>
    </p>
</xsl:template>
    
<!-- archéo -->    
<xsl:template match="text:p[starts-with(@text:style-name,'adarcheoA-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adarcheoA-')]/@style:name]" mode="front">
    <p>
    	<xsl:attribute name="n">
            <xsl:number count="text:p" from="office:text"/>
        </xsl:attribute>
        <xsl:attribute name="style">
            <xsl:value-of select="concat('archeo_',substring-after(@text:style-name,'adarcheoA-'))"/>
        </xsl:attribute>
        <xsl:apply-templates/>
    </p>
</xsl:template>

<!-- liens données, liens publications -->    
<xsl:template match="text:p[starts-with(@text:style-name,'adlien-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adlien-')]/@style:name]" mode="front">
    <p>
    	<xsl:attribute name="n">
            <xsl:number count="text:p" from="office:text"/>
        </xsl:attribute>
        <xsl:attribute name="style">
            <xsl:value-of select="concat('lien_',substring-after(@text:style-name,'adlien-'))"/>
        </xsl:attribute>
        <xsl:apply-templates/>
    </p>
</xsl:template>

<!-- organisation de soutien : partenaires, financeurs -->    
<xsl:template match="text:p[starts-with(@text:style-name,'adorg-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adorg-')]/@style:name]" mode="front">
    <p>
    	<xsl:attribute name="n">
            <xsl:number count="text:p" from="office:text"/>
        </xsl:attribute>
        <xsl:attribute name="style">
            <xsl:value-of select="concat('org_',substring-after(@text:style-name,'adorg-'))"/>
        </xsl:attribute>
        <xsl:apply-templates/>
    </p>
</xsl:template>
    
<!-- hors du mode "front", aucun traitement appliqué -->
<xsl:template match="text:p[@text:style-name='admotscles']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='admotsclesital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotsclesital']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='admotscles_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles_5f_inv']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adresume']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adresumeital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresumeital']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adresume_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume_5f_inv']/@style:name]"/>

    
<xsl:template match="text:p[starts-with(@text:style-name,'note_3a_')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'noe_3a_')]/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adchapo']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adchapo']/@style:name]"/>

<xsl:template match="text:p[@text:style-name='addedicace']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addedicace']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adremerciements']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adremerciements']/@style:name]"/>

<xsl:template match="text:p[starts-with(@text:style-name,'adarcheoA-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adarcheoA-')]/@style:name]"/>
<xsl:template match="text:p[starts-with(@text:style-name,'adlien-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adlien-')]/@style:name]"/>
<xsl:template match="text:p[starts-with(@text:style-name,'adorg-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adorg-')]/@style:name]"/>

</xsl:stylesheet>