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
    
<xsl:template match="text:p[@text:style-name='adtitrefigure']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitrefigure']/@style:name]">
    <xsl:choose>
        <xsl:when test="preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]"></xsl:when>
        <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adouvrage_5f_refbibliofull')]/@style:name]"></xsl:when>
        <xsl:otherwise>
  <figure>
    <xsl:if test="child::text:bookmark">
          <xsl:attribute name="xml:id">
              <xsl:value-of select="child::text:bookmark/@text:name"/>
          </xsl:attribute>
      </xsl:if>
		<xsl:if test="descendant::text:span[@text:style-name='adCAnumill']">
			<xsl:attribute name="n">
				<xsl:value-of select="descendant::text:span[@text:style-name='adCAnumill']"/>
			</xsl:attribute>
		</xsl:if>
		<xsl:apply-templates select="descendant::draw:frame"/>
		<head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a|text:note"/>
		</head>
<!-- après le titre [1] : légende -->
	<xsl:if test="following-sibling::text:p[1][@text:style-name='adlegendefigtab']">
		<p style="txt_Legende">
			<xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adlegendefigtab']" mode="inFigureCall"/>
		</p>
		<xsl:if test="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']">
			<p style="ill-credits-sources">
				<xsl:apply-templates select="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']" mode="inFigureCall"/>
			</p>
		</xsl:if>
	</xsl:if>
	<xsl:if test="text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adlegendefigtab']/@style:name]">
		<p style="txt_Legende">
			<xsl:apply-templates select="text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adlegendefigtab']/@style:name]" mode="inFigureCall"/>
		</p>
	</xsl:if>
  <!-- après le titre [1] : crédits sources -->
  	<xsl:if test="following-sibling::text:p[1][@text:style-name='adcredits-sources-ill']">
  		<p style="ill-credits-sources">
  			<xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adcredits-sources-ill']" mode="inFigureCall"/>
  		</p>
  	</xsl:if>
  	<xsl:if test="text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]">
  		<p style="ill-credits-sources">
  			<xsl:apply-templates select="text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]" mode="inFigureCall"/>
  		</p>
  	</xsl:if>
<!-- après le titre [2] : crédits sources 
	<xsl:if test="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']">
		<p style="ill-credits-sources">
			<xsl:apply-templates select="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']" mode="inFigureCall"/>
		</p>
	</xsl:if>-->
	<!--<xsl:if test="text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]">
		<p style="ill-credits-sources">
			<xsl:apply-templates select="text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]" mode="inFigureCall"/>
		</p>
	</xsl:if>-->
<!-- après le titre [2] : crédits-sources
	<xsl:if test="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]">
		<p style="ill-credits-sources">
			<xsl:apply-templates select="following-sibling::text:p[2][@text:style-name='adcredits-sources-ill']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]" mode="inFigureCall"/>
		</p>
	</xsl:if>-->
	</figure>
    </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adlegendefigtab']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adlegendefigtab']/@style:name]" mode="inFigureCall">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcredits-sources-ill']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]" mode="inFigureCall">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adlegendefigtab']">
	<xsl:if test="not(preceding-sibling::text:p[1][@text:style-name='adtitrefigure'])">
		<p style="txt_Legende">
			<xsl:apply-templates/>
		</p>
	</xsl:if>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcredits-sources-ill']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcredits-sources-ill']/@style:name]">
	<xsl:choose>
    <xsl:when test="preceding-sibling::text:p[1][@text:style-name='adtitretableau'] or preceding-sibling::text:p[2][@text:style-name='adtitretableau']">
      <p style="table-credits-sources">
        <xsl:apply-templates/>
      </p>
    </xsl:when>
    <xsl:otherwise/>
  </xsl:choose>
</xsl:template>

<!-- texte alternatif -->
<xsl:template match="svg:title"/>
    
<xsl:template match="svg:desc">
    <figDesc><xsl:apply-templates/></figDesc>
</xsl:template>

</xsl:stylesheet>