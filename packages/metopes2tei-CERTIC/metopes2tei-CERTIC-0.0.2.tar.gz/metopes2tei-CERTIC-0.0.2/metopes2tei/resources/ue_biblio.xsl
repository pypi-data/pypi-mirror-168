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

<!-- Bibliographie dans le back -->
<xsl:template name="biblioBack">
	<div type="bibliographie">
		<head style="T_1">
			<xsl:apply-templates select="text:p[@text:style-name='Titre-section-biblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-biblio']/@style:name]"/>
		</head>
<!-- test du premier nœud suivant pour déterminer sa nature -->
<xsl:variable name="nextNode"><xsl:value-of select="."/></xsl:variable>
<!--xsl:comment><xsl:value-of select="text:p[@text:style-name='Titre-section-biblio']/following::*[1]/local-name()"/></xsl:comment-->
<xsl:variable name="nextHeadNode"><xsl:value-of select="text:p[@text:style-name='Titre-section-biblio']/following::text:h[1]"/></xsl:variable>
<xsl:choose>
	<xsl:when test="$nextNode='h'">
		<!--xsl:comment>following is a title</xsl:comment-->
	</xsl:when>
	<xsl:otherwise>
		<!--xsl:comment>following is a bibl</xsl:comment>
		<xsl:comment>nextHead = <xsl:value-of select="$nextHeadNode"/></xsl:comment-->
		<xsl:for-each select="text:p[@text:style-name='Titre-section-biblio']/following-sibling::text:p[@text:style-name='adbiblio'][following::text:h[@text:outline-level][1] = $nextHeadNode]|text:p[@text:style-name='Titre-section-biblio']/following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][following::text:h[@text:outline-level][1] = $nextHeadNode]">
			<bibl style="txt_Bibliographie" type="orig">
				<xsl:attribute name="xml:id">
                	<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            	</xsl:attribute>
     	   		<xsl:apply-templates/>
      		</bibl>
		</xsl:for-each>
	</xsl:otherwise>
</xsl:choose>
<xsl:choose>
<!-- test présence d'un titre de niveau 3 -->
	<xsl:when test="text:p[@text:style-name='Titre-section-biblio']/following-sibling::text:h[@text:outline-level='3']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-biblio']/@style:name]/following-sibling::text:h[@text:outline-level='3']">
<!-- tester si références biblio avant le premier T3 -->
<xsl:for-each select="text:p[@text:style-name='Titre-section-biblio']/following-sibling::text:h[@text:outline-level='3']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-biblio']/@style:name]/following-sibling::text:h[@text:outline-level='3']">
<xsl:variable name="headBibl" select="."/>
	<listBibl>
		<!--xsl:comment>niveau de titre 3</xsl:comment-->
		<head style="T_2" subtype="level2"><xsl:apply-templates/></head>
		<!--xsl:comment>headBibl = <xsl:value-of select="$headBibl"/></xsl:comment-->
    	<xsl:for-each select="following-sibling::text:p[@text:style-name='adbiblio'][preceding-sibling::text:h[@text:outline-level][1] = $headBibl]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:h[@text:outline-level][1] = $headBibl]">
  		<bibl style="txt_Bibliographie" type="orig">
  			<xsl:attribute name="xml:id">
              	<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            </xsl:attribute>
     	   <xsl:apply-templates/>
      	</bibl>
    </xsl:for-each>

<!-- niveau de titre 4 -->
<xsl:if test="following-sibling::text:h[@text:outline-level='4']">
	<xsl:for-each select="following-sibling::text:h[@text:outline-level='4'][preceding-sibling::text:h[@text:outline-level='3'][1] = $headBibl]">
		<xsl:variable name="headBibl2" select="."/>
		<xsl:variable name="following-title" select="following::text:h[@text:outline-level='4']"/>
		<xsl:variable name="following-titleLevel" select="following::text:h[1]/@text:outline-level"/>
		<listBibl>
			<!--xsl:comment>niveau de titre 4</xsl:comment-->
			<head style="T_3" subtype="level3"><xsl:apply-templates/></head>
				<!--xsl:comment>headBibl = <xsl:value-of select="$headBibl"/></xsl:comment>
				<xsl:comment>headBibl2 = <xsl:value-of select="$headBibl2"/></xsl:comment>
				<xsl:comment>following-title = <xsl:value-of select="$following-title"/></xsl:comment>
				<xsl:comment>following-titleLevel = <xsl:value-of select="$following-titleLevel"/></xsl:comment-->
			
			<xsl:choose>
				<xsl:when test="$following-titleLevel='4'">
					<xsl:for-each select="following-sibling::text:p[@text:style-name='adbiblio'][preceding-sibling::text:h[@text:outline-level='4'][1] = $headBibl2]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:h[@text:outline-level='4'][1] = $headBibl2]">
						<bibl style="txt_Bibliographie" type="orig">
							<xsl:attribute name="xml:id">
                				<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            				</xsl:attribute>
							<xsl:apply-templates/>
						</bibl>
					</xsl:for-each>
				</xsl:when>
				<xsl:otherwise>
					<!--xsl:comment>no following level 4 title</xsl:comment-->
					<xsl:for-each select="following-sibling::text:p[@text:style-name='adbiblio'][preceding-sibling::text:h[@text:outline-level='3'][1] = $headBibl]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:h[@text:outline-level='3'][1] = $headBibl]">
						<bibl style="txt_Bibliographie" type="orig">
							<xsl:attribute name="xml:id">
                				<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            				</xsl:attribute>
							<xsl:apply-templates/>
						</bibl>
					</xsl:for-each>
				</xsl:otherwise>
			</xsl:choose>			
		</listBibl>
	</xsl:for-each>
</xsl:if>
<!-- fin niveau de titre 4 -->			
			
			<!--xsl:for-each select="following-sibling::text:p[@text:style-name='adbiblio'][preceding-sibling::text:h[@text:outline-level='3'][1] = $headBibl][not(preceding-sibling::text:h[@text:outline-level='4'])]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:h[@text:outline-level='3'][1] = $headBibl][not(preceding-sibling::text:h[@text:outline-level='4'])]">
			<xsl:variable name="simpleBibl" select="."/>
				<bibl style="txt_Bibliographie">|
					<xsl:apply-templates/>
				</bibl>
				<xsl:for-each select="following-sibling::text:p[@text:style-name='adbibliosuite'][preceding-sibling::text:p[@text:style-name='adbiblio'][1] = $simpleBibl]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbibliosuite']/@style:name][preceding-sibling::text:p[@text:style-name='adbiblio'][1] = $simpleBibl]">
					<bibl style="txt_Bibliographie_suite">
						<xsl:apply-templates/>
					</bibl>
				</xsl:for-each>
			</xsl:for-each-->

	</listBibl>
	</xsl:for-each>
</xsl:when>

<!-- Bibliographie sans sous-structure -->
<xsl:when test="text:p[@text:style-name='adbiblio'][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]">
	<listBibl>
		<xsl:for-each select="text:p[@text:style-name='adbiblio'][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]">
		<!--xsl:variable name="simpleBibl" select="."/-->
			<bibl style="txt_Bibliographie" type="orig">
				<xsl:attribute name="xml:id">
                	<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            	</xsl:attribute>
				<xsl:apply-templates/>
			</bibl>
		</xsl:for-each>
	</listBibl>
	</xsl:when>

</xsl:choose>
</div>
</xsl:template>

<xsl:template match="text:p[@text:outline-level][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]"/>

<xsl:template match="text:p[@text:style-name='adbiblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]">
<xsl:choose>
	<xsl:when test="following-sibling::text:p[@text:style-name='Titre-section-biblio']">
		<bibl style="txt_Bibliographie" type="orig">
			<xsl:attribute name="xml:id">
                	<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            	</xsl:attribute>
			<xsl:apply-templates/>
		</bibl>
	</xsl:when>
	<xsl:when test="not(preceding-sibling::text:p[@text:style-name='Titre-section-biblio'])">
		<bibl style="txt_Bibliographie" type="orig">
			<xsl:attribute name="xml:id">
                	<xsl:value-of select="concat('bibl', format-number(count(preceding::text:p[@text:style-name='adbiblio']) +count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbiblio']/@style:name]) + 1,'00'))"/>
            	</xsl:attribute>
			<xsl:apply-templates/>
		</bibl>
	</xsl:when>
	<xsl:otherwise>
	</xsl:otherwise>
</xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adbibliosuite']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adbibliosuite']/@style:name]">
</xsl:template>

</xsl:stylesheet>