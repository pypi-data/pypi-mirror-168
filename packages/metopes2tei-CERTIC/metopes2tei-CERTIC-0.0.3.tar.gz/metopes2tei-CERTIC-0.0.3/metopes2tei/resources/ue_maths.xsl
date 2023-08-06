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
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
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

<!-- xmlns:math="http://www.w3.org/1998/Math/MathML" -->

<xsl:template match="math:*">
  <xsl:element name="mml:{local-name()}">
    <xsl:copy-of select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>


<xsl:template match="text:p[@text:style-name='adtex']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtex']/@style:name]">
  <p rend="block" style="tex">
  	<formula notation="tex" rend="block">
      <xsl:apply-templates/>
    </formula>
  </p>
</xsl:template>

<xsl:template match="text:span[@text:style-name='adCAtex']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAtex']/@style:name]">
	<formula notation="tex" rend="inline">
		<xsl:apply-templates/>
	</formula>
</xsl:template>

<xsl:template match="draw:object[child::*:math]">
  <xsl:choose>
    <xsl:when test="ancestor::text:p[@text:style-name='admml']|ancestor::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admml']/@style:name]">
      <p rend="block" style="mathml">
        <formula notation="mml" rend="block">
          <xsl:apply-templates/>
        </formula>
      </p>
    </xsl:when>
    <xsl:otherwise>
      <formula notation="mml" rend="inline">
        <xsl:apply-templates/>
      </formula>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


</xsl:stylesheet>
