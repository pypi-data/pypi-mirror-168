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

<xsl:template name="paraAuteurs">
    <xsl:apply-templates select="//text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]" mode="header"/>
</xsl:template>
    
<xsl:template name="paraCollaborateurs">
    <xsl:apply-templates select="//text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]" mode="header"/>
</xsl:template>

<xsl:template match="text:span[@text:style-name='adCAauteur']" mode="header">
<xsl:variable name="here" select="."/>
<xsl:variable name="there" select="following-sibling::text:span[@text:style-name='adCAauteur'][1]"/>
    <xsl:choose>
        <xsl:when test="ancestor::text:p[@text:style-name='adauteurs']|ancestor::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]">
    <author role="aut">
        <name><xsl:apply-templates/></name>
        <xsl:choose>
            <xsl:when test="not($there) and following-sibling::text:span[@text:style-name='adCAaffiliation']">
                <xsl:variable name="affCount" select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                <affiliation>       
                    <ref type="affiliation">
                        <xsl:attribute name="target">
                            <xsl:choose>
                                <xsl:when test="$affCount &lt; 10">
                                    <xsl:value-of select="concat('#aff0',$affCount)"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="concat('#aff',$affCount)"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:attribute>
                    </ref>
                </affiliation>
            </xsl:when>
            <xsl:when test="$there and not(following-sibling::text:span[@text:style-name='adCAaffiliation'])">
            </xsl:when>
            <xsl:when test="not($there) and not(following-sibling::text:span[@text:style-name='adCAaffiliation'])">
            </xsl:when>
            <xsl:otherwise>
                <xsl:for-each select="following-sibling::text:span[@text:style-name='adCAaffiliation'][following-sibling::text:span[@text:style-name='adCAauteur']=$there]">
                    <xsl:variable name="affCount" select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                    <affiliation>
                        <ref type="affiliation">
                            <xsl:attribute name="target">
                                <xsl:choose>
                                    <xsl:when test="$affCount &lt; 10">
                                        <xsl:value-of select="concat('#aff0',$affCount)"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="concat('#aff',$affCount)"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:attribute>
                        </ref>
                    </affiliation>
                </xsl:for-each>
            </xsl:otherwise>
        </xsl:choose> 
    </author>
        </xsl:when>
        <xsl:otherwise>
            <editor role="##">
                <name><xsl:apply-templates/></name>
        <!--        <xsl:apply-templates mode="header"/>-->
                <xsl:choose>
                    <xsl:when test="not($there) and following-sibling::text:span[@text:style-name='adCAaffiliation']">
                        <xsl:variable name="affCount" select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                        <affiliation>
                            <ref type="affiliation">
                                <xsl:attribute name="target">
                                    <xsl:choose>
                                        <xsl:when test="$affCount &lt; 10">
                                            <xsl:value-of select="concat('#aff0',$affCount)"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="concat('#aff',$affCount)"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:attribute>
                            </ref>
                        </affiliation>
                    </xsl:when>
                    <xsl:when test="$there and not(following-sibling::text:span[@text:style-name='adCAaffiliation'])">
                    </xsl:when>
                    <xsl:when test="not($there) and not(following-sibling::text:span[@text:style-name='adCAaffiliation'])">
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="following-sibling::text:span[@text:style-name='adCAaffiliation'][following-sibling::text:span[@text:style-name='adCAauteur']=$there]">
                            <xsl:variable name="affCount" select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                            <affiliation>
                                <ref type="affiliation">
                                    <xsl:attribute name="target">
                                        <xsl:choose>
                                            <xsl:when test="$affCount &lt; 10">
                                                <xsl:value-of select="concat('#aff0',$affCount)"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="concat('#aff',$affCount)"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:attribute>
                                </ref>
                            </affiliation>
                        </xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose> 
            </editor>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
    
<xsl:template match="text:span[@text:style-name='adCAArcheoresponsable']" mode="header">
<xsl:variable name="here" select="."/>
<xsl:variable name="there" select="following-sibling::text:span[@text:style-name='adCAArcheoresponsable'][1]"/>
    <xsl:choose>
        <xsl:when test="parent::text:p[@text:style-name='adauteurs']">
            <author role='fld'>
                <name><xsl:apply-templates mode="header"/></name>
            </author>
        </xsl:when>
        <xsl:when test="parent::text:p[@text:style-name='adcollaborateurs']">
            <editor role='fld'>
                <name><xsl:apply-templates mode="header"/></name>
                <xsl:choose>
            		<xsl:when test="not($there)">
                		<affiliation>       
                    		<xsl:value-of select="following-sibling::text:span[@text:style-name='adCAaffiliation']"/>
                		</affiliation>
            		</xsl:when>
            		<xsl:otherwise>
                		<xsl:for-each select="following-sibling::text:span[@text:style-name='adCAaffiliation'][following-sibling::text:span[@text:style-name='adCAArcheoresponsable']=$there]">
                    		<affiliation>
                        		<xsl:value-of select="."/>
                    		</affiliation>
                		</xsl:for-each>
            		</xsl:otherwise>
        		</xsl:choose> 
            </editor>
        </xsl:when>
        <xsl:otherwise>
            <xsl:text>???</xsl:text>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="text:span[@text:style-name='adCAaffiliation']|text:span[starts-with(@text:style-name,'T')]|text:p[@text:style-name='adauteurs']/text()|text:p[@text:style-name='adcollaborateurs']/text()" mode="header"/>
       
</xsl:stylesheet>
