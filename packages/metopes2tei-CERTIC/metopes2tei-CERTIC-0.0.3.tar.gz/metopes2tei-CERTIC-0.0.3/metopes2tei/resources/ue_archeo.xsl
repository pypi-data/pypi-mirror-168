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

 <xsl:key name="biblFollowing" match="text:p[@text:style-name='adArcheobiblio'][preceding-sibling::*[1][self::text:p[@text:style-name='adArcheobiblio']]]" use="generate-id(preceding-sibling::text:p[@text:style-name='adArcheobiblio'][not(preceding-sibling::*[1][self::text:p[@text:style-name='adArcheobiblio']])][1])"/>
    
<!-- autorités -->
<xsl:template match="text:span[starts-with(@text:style-name,'adCAArcheo')]|text:span[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adCAArcheo')]/@style:name]">
  <xsl:choose>
    <xsl:when test="@text:style-name='adCAArcheocoordinateur' or @style:parent-style-name='adCAArcheocoordinateur'">
      <name role="edt">
        <xsl:apply-templates/>
      </name>
    </xsl:when>
    <xsl:when test="@text:style-name='adCAArcheoresponsable' or @style:parent-style-name='adCAArcheoresponsable'">
      <name role="fld">
        <xsl:apply-templates/>
      </name>
    </xsl:when>
    <xsl:when test="@text:style-name='adCAArcheoredacteur' or @style:parent-style-name='adCAArcheoredacteur'">
      <name role="aut">
        <xsl:apply-templates/>
      </name>
    </xsl:when>
    <xsl:when test="@text:style-name='adCAArcheoauteurresp' or @style:parent-style-name='adCAArcheoauteurresp'">
      <name role="aut fld">
        <xsl:apply-templates/>
      </name>
    </xsl:when>
    <xsl:otherwise>
      <name role="##">
        <xsl:apply-templates/>
      </name>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- affiliation -->
<xsl:template match="text:span[@text:style-name='adCAaffiliation']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAaffiliation']/@style:name]" mode="front">
    <xsl:variable name="AffId">
        <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation']|preceding::text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAaffiliation']/@style:name]) +1"/>
    </xsl:variable>
    <affiliation>
        <xsl:attribute name="xml:id">
            <xsl:choose>
                <xsl:when test="$AffId &lt; 10">
                    <xsl:value-of select="concat('aff0',$AffId)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat('aff',$AffId)"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <xsl:apply-templates/>
    </affiliation>
</xsl:template>
    
<xsl:template match="text:span[@text:style-name='adCAaffiliation']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAaffiliation']/@style:name]">
    <xsl:variable name="AffId">
        <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation']|preceding::text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAaffiliation']/@style:name]) +1"/>
    </xsl:variable>
    <affiliation>
        <xsl:attribute name="xml:id">
                    <xsl:choose>
                        <xsl:when test="$AffId &lt; 10">
                            <xsl:value-of select="concat('aff0',$AffId)"/>
                        </xsl:when>
                        <xsl:otherwise>
            <xsl:value-of select="concat('aff',$AffId)"/>
                        </xsl:otherwise>
                    </xsl:choose>
        </xsl:attribute>
        <xsl:apply-templates/>
    </affiliation>
</xsl:template>

<!-- paragraphe d'autorités -->
<xsl:template match="text:p[@text:style-name='adArcheoautorites']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheoautorites']/@style:name]">
	<p style="txt_archeo_autorites" rendition="none">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
  
<!-- sous-titre -->
<xsl:template match="text:p[@text:style-name='adArcheosoustitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheosoustitre']/@style:name]">
	<head style="T_sub" type="sub">
		<xsl:apply-templates/>
	</head>
</xsl:template>
    
<!-- liste de mots-clés (non présents dans le texte) -->
<xsl:template match="text:p[@text:style-name='adArcheomcindex']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheomcindex']/@style:name]">
	<p style="txt_archeo_mc" rendition="none">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
<!-- mots-clés chronologique -->
<xsl:template match="text:p[@text:style-name='adArcheochrono']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheochrono']/@style:name]">
	<p style="txt_archeo_mc_chrono" rendition="none">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
<!-- renvoi -->
<xsl:template match="text:p[@text:style-name='adArcheorenvoi']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheorenvoi']/@style:name]">
	<p style="txt_archeo_renvoi" rendition="print">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
<!-- lien rapport -->
<xsl:template match="text:p[@text:style-name='adArcheorapport']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheorapport']/@style:name]">
	<p style="txt_archeo_rapport" rendition="oe">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
<!-- organisme porteur -->
<xsl:template match="text:p[@text:style-name='adArcheoorg']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheoorg']/@style:name]">
	<p style="txt_archeo_org" rendition="oe">
		<xsl:apply-templates/>
	</p>
</xsl:template>

<!-- Année d'opération -->
<xsl:template match="text:p[@text:style-name='adArcheoOpAnnee']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheoOpAnnee']/@style:name]">
	<ab type="meta-archeo" rendition="none">
        <xsl:value-of select="concat(substring-before(., ': '),': ')"/>
        <xsl:variable name="anneeOP" select="substring-after(., ': ')" />
        <xsl:call-template name="anneeList">
            <xsl:with-param name="list">
                <xsl:value-of select="$anneeOP"/>
            </xsl:with-param>
        </xsl:call-template>
	</ab>
</xsl:template>

<xsl:template name="anneeList">
    <xsl:param name="list"/>
    <xsl:variable name="first" select="substring-before($list, ', ')" />
    <xsl:variable name="remaining" select="substring-after($list, ', ')" />
    <xsl:choose>
        <xsl:when test="$first">
            <date><xsl:value-of select="$first"/></date>
            <xsl:if test="$remaining">
                <xsl:call-template name="anneeList">
                    <xsl:with-param name="list" select="$remaining" />
                </xsl:call-template>
            </xsl:if>
        </xsl:when>
        <xsl:otherwise>
            <date><xsl:value-of select="$list"/></date>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Nature d'opération -->
<xsl:template match="text:p[@text:style-name='adArcheoOpNature']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheoOpNature']/@style:name]">
	<p style="txt_archeo_natureOp" rendition="print">
		<xsl:apply-templates/>
	</p>
</xsl:template>
    
<!-- ID patriarche -->
<xsl:template match="text:p[@text:style-name='adArcheoIDpatriarche']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adArcheoIDpatriarche']/@style:name]">
	<p style="txt_archeo_IDpatriarche" rendition="none">
        <xsl:analyze-string select="." regex="(\d+)">
          <xsl:matching-substring>
            <idno type="patriarche"><xsl:value-of select="."/></idno>
          </xsl:matching-substring>
          <xsl:non-matching-substring>
              <xsl:value-of select="."/>
          </xsl:non-matching-substring>
        </xsl:analyze-string>
    </p>
</xsl:template>

<!-- biblio -->
<xsl:template match="text:p[@text:style-name='adArcheobiblio']" name="biblioArcheo">
  <bibl>
   <xsl:apply-templates/>
  </bibl>
 </xsl:template>

 <xsl:template match="text:p[@text:style-name='adArcheobiblio'][not(preceding-sibling::*[1][self::text:p[@text:style-name='adArcheobiblio']])]">
  <listBibl>
    <xsl:call-template name="biblioArcheo"/>
    <xsl:apply-templates mode="copy" select="key('biblFollowing', generate-id())"/>
  </listBibl>
 </xsl:template>

 <xsl:template match="text:p[@text:style-name='adArcheobiblio'][preceding-sibling::*[1][self::text:p[@text:style-name='adArcheobiblio']]]"/>

 <xsl:template match="text:p[@text:style-name='adArcheobiblio']" mode="copy">
  <xsl:call-template name="biblioArcheo"/>
 </xsl:template>

</xsl:stylesheet>