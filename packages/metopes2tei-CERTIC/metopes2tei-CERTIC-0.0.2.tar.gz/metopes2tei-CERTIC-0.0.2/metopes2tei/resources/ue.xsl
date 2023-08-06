<?xml version="1.0" encoding="UTF-8"?>

<!--
 # oototei (P5), xslt stylesheet
 #
 # Copyright (c) 2009-2017
 #  Pôle Document Numérique
 #  Maison de la Recherche en Sciences Humaines
 #  Université de Caen Basse-Normandie
 #  Esplanade de la Paix
 #  Campus 1
 #  14032 Caen Cedex
 #
 # See http://www.unicaen.fr/recherche/mrsh/document_numerique/equipe
 # for a list of contributors
 #
 #  This stylesheet is derived from the work of Sebastian Rahtz / University of Oxford (copyright 2005)
 #
 #  This programme is free software; you can redistribute it and/or
 #  modify it under the terms of the GNU General Public
 #  License as published by the Free Software Foundation,
 #  either version 3 of the License, or
 #  (at your option) any later version.
 #
 #  This program is distributed in the hope that it will be useful,
 #  but WITHOUT ANY WARRANTY; without even the implied warranty of
 #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 #  Lesser General Public License for more details.
 #  <http://www.gnu.org/licenses/>
 #
-->

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
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0">

<xsl:include href="ue_recension.xsl"/>
<xsl:include href="ue_figures.xsl"/>
<xsl:include href="ue_front.xsl"/>
<xsl:include href="ue_biblio.xsl"/>
<xsl:include href="ue_maths.xsl"/>
<xsl:include href="ue_archeo.xsl"/>
<xsl:include href="ue_autorites.xsl"/>

  <xsl:key match="style:style" name="STYLES" use="@style:name"/>

  <xsl:key name="LISTS"
	 match="text:list-level-style-number"
	 use="parent::text:list-style/@style:name"/>

  <xsl:key match="text:h" name="Headings" use="text:outline-level"/>

  <xsl:key name="MetaUserDefined" match="meta:user-defined" use="@meta:name"/>

  <xsl:key name="secondary_children" match="text:p[@text:style-name =
'Index 2']"
use="generate-id(preceding-sibling::text:p[@text:style-name = 'Index
1'][1])"/>

  <xsl:key name="auteurs" match="text:p[@text:style-name='adauteur']" use="generate-id(following-sibling::text:p[@text:style-name='adinstitution'][1])"/>

  <xsl:param name="debug">false</xsl:param>

  <xsl:output method="xml" encoding="utf-8" indent="no"/>

  <!-- <xsl:strip-space elements="text:span"/> -->

  <xsl:variable name="META">
    <xsl:choose>
      <!--xsl:when test="doc-available(concat($dir,'/meta.xml'))">
        <xsl:copy-of select="document(concat($dir,'/meta.xml'))//office:meta"/>
      </xsl:when-->
      <xsl:when test="/office:document/office:meta">
        <xsl:copy-of select="/office:document/office:meta"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="/office:document-meta/office:meta"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

	<xsl:variable name="OOstyles">
		<xsl:choose>
			<xsl:when test="/office:document/office:automatic-styles">
				<xsl:copy-of select="/office:document/office:automatic-styles"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="/office:document/office:automatic-styles"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

  <xsl:variable name="document-title">
    <xsl:choose>
      <xsl:when
	  test="/office:document-content/office:body/office:text/text:p[@text:style-name='Title | Titre 1']">
        <xsl:value-of
	    select="/office:document-content/office:body/office:text/text:p[@text:style-name='Title | Titre 1'][1]/text()"
	    />
      </xsl:when>
  <!--    <xsl:when test="$META/office:meta/dc:title">
        <xsl:value-of select="$META/office:meta/dc:title"/>
      </xsl:when>
      <xsl:when test="/office:document/office:meta/dc:title">
        <xsl:value-of select="/office:document/office:meta/dc:title"/>
      </xsl:when> -->
      <xsl:when test="//text:h[@text:outline-level='1'][1]">
        <xsl:apply-templates select="//text:h[@text:outline-level='1'][1]/text()|//text:h[@text:outline-level='1']/text:span[@text:style-name]/text()"/>
      </xsl:when>
      <xsl:when test="//text:p[@text:style-name='Titre-recension']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-recension']/@style:name]">
        <xsl:apply-templates select="//text:p[@text:style-name='Titre-recension']/node()|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-recension']/@style:name]/node()"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>Untitled Document</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:template match="/">
    <xsl:if test="$debug='true'">
      <xsl:message>Look for metadata in <!--xsl:value-of select="concat($dir,'/meta.xml')"/--></xsl:message>
    </xsl:if>
    <xsl:variable name="pass1">
      <xsl:apply-templates/>
    </xsl:variable>
    <xsl:variable name="pass2">
      <xsl:apply-templates mode="pass2" select="$pass1"/>
    </xsl:variable>
    <xsl:apply-templates mode="pass3" select="$pass2"/>
  </xsl:template>

  <xsl:template match="office:document-content|office:body">
    <xsl:for-each select="descendant::text:variable-decl">
      <xsl:variable name="name">
        <xsl:value-of select="@text:name"/>
      </xsl:variable>
      <xsl:if test="contains(@text:name,'entitydecl')">
        <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE TEI [
	</xsl:text>
        <xsl:text disable-output-escaping="yes">&lt;!ENTITY </xsl:text>
        <xsl:value-of select="substring-after(@text:name,'entitydecl_')"/>
        <xsl:text> &quot;</xsl:text>
        <xsl:value-of
          select="/descendant::text:variable-set[@text:name= $name][1]"/>
        <xsl:text disable-output-escaping="yes">&quot;&gt;</xsl:text>
        <xsl:text disable-output-escaping="yes">]&gt;</xsl:text>
      </xsl:if>
    </xsl:for-each>
    <TEI change="metopes_edition">
	<xsl:for-each select="$META/office:meta/dc:language">
	  <xsl:attribute name="xml:lang">
	    <xsl:value-of select="normalize-space(.)"/>
	  </xsl:attribute>
	</xsl:for-each>
      <xsl:call-template name="teiHeader"/>
      <text xml:id="text">
	<xsl:apply-templates/>
      </text>
    </TEI>
  </xsl:template>

<!-- header des unités éditoriales -->
<xsl:template name="teiHeader">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="main">
          <xsl:value-of select="$document-title"/>
        </title>
        <xsl:if test="//text:p[@text:style-name='adtitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitre_5f_inv']/@style:name]">
        	<title type="alt" xml:lang="##" rend="rtl">
        		<xsl:value-of select="//text:p[@text:style-name='adtitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitre_5f_inv']/@style:name]"/>
        	</title>
        </xsl:if>
        <xsl:if test="//text:p[@text:style-name='adSousTitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adSousTitre']/@style:name]">
        	<title type="sub">
        		<xsl:value-of select="//text:p[@text:style-name='adSousTitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adSousTitre']/@style:name]"/>
        	</title>
        </xsl:if>
        <xsl:if test="//text:p[@text:style-name='adsoustitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsoustitre_5f_inv']/@style:name]">
        	<title type="sub" xml:lang="##" rend="rtl">
        		<xsl:value-of select="//text:p[@text:style-name='adsoustitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsoustitre_5f_inv']/@style:name]"/>
        	</title>
        </xsl:if>
        <!--xsl:if test="//text:p[@text:style-name='adTitreTraduit']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTitreTraduit']/@style:name]"-->
        	<xsl:for-each select="//text:p[@text:style-name='adTitreTraduit']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTitreTraduit']/@style:name]">
    			<xsl:variable name="title-trad">
    				<xsl:value-of select="."/>
    			</xsl:variable>
        	<title type="alt" xml:lang="##">
        		 <xsl:value-of select="$title-trad"/>
        	</title>
        	</xsl:for-each>
        <!--/xsl:if-->
          <xsl:for-each select="//text:p[@text:style-name='adauteur']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteur']/@style:name]">
            <xsl:variable name="author">
				<xsl:value-of select=".//text()[not(ancestor::text:note) and not(ancestor::text:span[@text:style-name='adCAneutral'])]"/>
			</xsl:variable>
            <author role="aut"><!--<xsl:apply-templates select="key('auteurs',generate-id(.))" mode="header"/><xsl:apply-templates select="." mode="header"/>-->
            	<name><xsl:value-of select="$author"/></name>
            <xsl:if test="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name]">
            	<affiliation>
            		<xsl:value-of select="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name][1]"/>
            	</affiliation>
            </xsl:if>
<!-- plusieurs paragraphes de rattachement après le nom de l'auteur mais sans adCAaffiliation (scénario 1) -->  
            <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][not(child::text:span[@text:style-name='adCAaffiliation'])]">
                <xsl:variable name="testNext">
                    <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
                </xsl:variable>
                <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]">
                    <xsl:variable name="affCount">
                        <xsl:value-of select="count(preceding::text:p[@text:style-name='adrattachement'])+1"/>
                    </xsl:variable>
                    <affiliation><!--<xsl:comment>*8*</xsl:comment>-->
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
            </xsl:if>
    <!-- plusieurs paragraphes de rattachement après le nom de l'auteur : affiliations isolées via le style de caractères adCAaffiliation (scénario bspf) -->
             <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][child::text:span[@text:style-name='adCAaffiliation']][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][child::text:span[@text:style-name='adCAaffiliation']]">
                <xsl:variable name="testNext">
                            <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
                </xsl:variable>
                <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]/text:span[@text:style-name='adCAaffiliation']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][following-sibling::text:p=$testNext]/text:span[@text:style-name='adCAaffiliation']">
                    <xsl:variable name="affCount">
                        <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                    </xsl:variable>
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
            </xsl:if>   
        	</author>
          </xsl:for-each>
          <xsl:for-each select="//text:p[@text:style-name='adcollaborateur']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateur']/@style:name]">
            <editor role="##"><name><xsl:apply-templates select=".//text()[not(ancestor::text:note) and not(ancestor::text:span[@text:style-name='adCAneutral'])]"/></name>
            <xsl:if test="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name]">
            	<affiliation>
            		<xsl:value-of select="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name]"/>
            	</affiliation>
            </xsl:if>
        <!-- cas bspf pour les collaborateurs -->
            <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][child::text:span[@text:style-name='adCAaffiliation']][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][child::text:span[@text:style-name='adCAaffiliation']]">
                <xsl:variable name="testNext">
                   <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
                </xsl:variable>
                <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]/text:span[@text:style-name='adCAaffiliation']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][following-sibling::text:p=$testNext]/text:span[@text:style-name='adCAaffiliation']">
                    <xsl:variable name="affCount">
                        <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                    </xsl:variable>
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
            </xsl:if> 
            <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][not(child::text:span[@text:style-name='adCAaffiliation'])]">
                <xsl:variable name="testNext">
                    <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
                </xsl:variable>
                <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]">
                    <xsl:variable name="affCount">
                        <xsl:value-of select="count(preceding::text:p[@text:style-name='adrattachement'])+1"/>
                    </xsl:variable>
                    <affiliation><!--<xsl:comment>*8*</xsl:comment>-->
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
            </xsl:if>
            </editor>
          </xsl:for-each>
        <!-- paragraphe auteurs -->
        <xsl:if test="//text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]">
             <xsl:call-template name="paraAuteurs"/>
         </xsl:if>
        <xsl:if test="//text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]">
             <xsl:call-template name="paraCollaborateurs"/>
         </xsl:if>
      </titleStmt>
      <editionStmt>
        <edition>
          <date>
            <xsl:value-of select="/office:document/office:meta/meta:creation-date"/>
          </date>
        </edition>
    	<xsl:if test="//text:p[@text:style-name='adorg-fin']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adorg-fin']/@style:name]">
        	<xsl:for-each select="//text:p[@text:style-name='adorg-fin']/text:span[@text:style-name='adCAFunder']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adorg-fin']/@style:name]/text:span[@text:style-name='adCAFunder']">
        		<funder>
        			<name><xsl:value-of select="."/></name>
        			<xsl:if test="following-sibling::text:span[@text:style-name='adCAFundRef']">
        				<idno><xsl:value-of select="./following-sibling::text:span[@text:style-name='adCAFundRef'][1]"/></idno>
        			</xsl:if>
        		</funder>
        	</xsl:for-each>
        </xsl:if>
      </editionStmt>
      <publicationStmt>
          <publisher></publisher>
      	<!--ab>Utilisation du fichier</ab-->
          <ab type="papier">
            <dimensions>
              <dim type="pagination"></dim>
            </dimensions>
            <date></date>
          </ab>
          <idno type="book"></idno>
          <ab type="lodel">
            <date></date>
          </ab>
          <xsl:if test="//text:p[starts-with(@text:style-name,'adarcheoA-IDmission')]|//text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adarcheoA-IDmission')]/@style:name]|//text:p[@text:style-name='adarcheoA-DatesOP']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adarcheoA-DatesOP']/@style:name]">
          	<ab type="archeo">
          		<idno>
          			<xsl:attribute name="type">
          				<xsl:value-of select="substring-after(//text:p[starts-with(@text:style-name,'adarcheoA-IDmission')]/@text:style-name,'adarcheoA-IDmission')"/>
          			</xsl:attribute>
          			<xsl:value-of select="substring-after(//text:p[starts-with(@text:style-name,'adarcheoA-IDmission')]|//text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adarcheoA-IDmission')]/@style:name], ': ')"/>
          		</idno>
                <xsl:if test="//text:p[@text:style-name='adarcheoA-DatesOP']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adarcheoA-DatesOP']/@style:name]">
                    <xsl:variable name="dateOP" select="substring-after(//text:p[@text:style-name='adarcheoA-DatesOP']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adarcheoA-DatesOP']/@style:name],': ')"/>

                        <xsl:analyze-string select="$dateOP" regex="\d{{4}}">
                            <xsl:matching-substring>
                                <date>
                                    <xsl:value-of select="."/>
                                </date>
                            </xsl:matching-substring>
                            <xsl:non-matching-substring/>
                        </xsl:analyze-string>
                </xsl:if>
          	</ab>
          </xsl:if>
      </publicationStmt>
      <sourceDesc>
      	<p>Version Métopes : 3.0</p>
        <p><xsl:apply-templates select="/office:document/office:meta/meta:generator"/><xsl:text>Written by OpenOffice</xsl:text></p>
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <xsl:choose>
        <xsl:when test="$OOstyles//office:automatic-styles/style:style[child::style:table-cell-properties]">
        	<tagsDecl>
        		<xsl:for-each select="$OOstyles//office:automatic-styles/style:style[child::style:table-cell-properties]">
        			<rendition scheme="css">
        				<xsl:attribute name="xml:id">
        					<xsl:choose>
    							<xsl:when test="contains(@style:name,'Tableau')">
    								<xsl:value-of select="concat('Cell',substring-after(@style:name,'Tableau'))"/>
    							</xsl:when>
    							<xsl:when test="contains(@style:name,'Tabla')">
    								<xsl:value-of select="concat('Cell',substring-after(@style:name,'Tabla'))"/>
    							</xsl:when>
    							<xsl:when test="contains(@style:name,'Table')">
    								<xsl:value-of select="concat('Cell',substring-after(@style:name,'Table'))"/>
    							</xsl:when>
                  <xsl:when test="contains(@style:name,'Tabella')">
    								<xsl:value-of select="concat('Cell',substring-after(@style:name,'Tabella'))"/>
    							</xsl:when>
                  <xsl:when test="contains(@style:name,'Tabela')">
    								<xsl:value-of select="concat('Cell',substring-after(@style:name,'Tabela'))"/>
    							</xsl:when>
    							<xsl:otherwise>
    							</xsl:otherwise>
    						</xsl:choose>
        				</xsl:attribute>
        				<xsl:if test="child::style:table-cell-properties/@fo:border">
        					<xsl:variable name="border" select="child::style:table-cell-properties/@fo:border"/>
        					<xsl:choose>
        						<xsl:when test="$border='none'">
        							<xsl:text>border:none;</xsl:text>
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>border:</xsl:text><xsl:value-of select="$border"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@fo:border-bottom">
        					<xsl:variable name="borderBottom" select="child::style:table-cell-properties/@fo:border-bottom"/>
        					<xsl:choose>
        						<xsl:when test="$borderBottom=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>border-bottom:</xsl:text><xsl:value-of select="$borderBottom"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@fo:border-left">
        					<xsl:variable name="borderLeft" select="child::style:table-cell-properties/@fo:border-left"/>
        					<xsl:choose>
        						<xsl:when test="$borderLeft=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>border-left:</xsl:text><xsl:value-of select="$borderLeft"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@fo:border-right">
        					<xsl:variable name="borderRight" select="child::style:table-cell-properties/@fo:border-right"/>
        					<xsl:choose>
        						<xsl:when test="$borderRight=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>border-right:</xsl:text><xsl:value-of select="$borderRight"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@fo:border-top">
        					<xsl:variable name="borderTop" select="child::style:table-cell-properties/@fo:border-top"/>
    						<xsl:choose>
        						<xsl:when test="$borderTop=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>border-top:</xsl:text><xsl:value-of select="$borderTop"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@fo:background-color">
        					<xsl:variable name="borderBackground" select="child::style:table-cell-properties/@fo:background-color"/>
    	  					<xsl:choose>
        						<xsl:when test="$borderBackground=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>;background-color:</xsl:text><xsl:value-of select="$borderBackground"/>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        				<xsl:if test="child::style:table-cell-properties/@style:vertical-align">
        					<xsl:variable name="vertical-align" select="child::style:table-cell-properties/@style:vertical-align"/>
    	  					<xsl:choose>
        						<xsl:when test="$vertical-align=''">
        						</xsl:when>
        						<xsl:otherwise>
        							<xsl:text>;vertical-align:</xsl:text><xsl:value-of select="$vertical-align"/><xsl:text>;</xsl:text>
        						</xsl:otherwise>
        					</xsl:choose>
        				</xsl:if>
        			</rendition>
        		</xsl:for-each>
        	</tagsDecl>
        </xsl:when>
        <xsl:otherwise>
          <tagsDecl>
            <rendition scheme="css" xml:id="none">color:black;</rendition>
          </tagsDecl>
        </xsl:otherwise>
      </xsl:choose>
    </encodingDesc>
    <profileDesc>
      <langUsage>
        <language>
          <xsl:choose>
            <xsl:when test="/office:document/office:meta/dc:language">
              <xsl:attribute name="ident"><xsl:value-of select="/office:document/office:meta/dc:language"/></xsl:attribute><xsl:value-of select="/office:document/office:meta/dc:language"/></xsl:when>
              <xsl:otherwise>
                <xsl:attribute name="ident">##-##</xsl:attribute>
             </xsl:otherwise>
              </xsl:choose>
              <xsl:value-of select="/office:document/office:meta/dc:language"/>
            </language>
          </langUsage>
          <textClass>
            <xsl:if test="//text:p[@text:style-name='admotscles']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name]">
              <keywords scheme="keyword" xml:lang="##">
                <list>
                  <xsl:variable name="listFR" select="substring-after(//text:p[@text:style-name='admotscles']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name], ': ')" />
                  <xsl:call-template name="keyWordsList">
                    <xsl:with-param name="list">
                      <xsl:value-of select="$listFR"/>
                    </xsl:with-param>
                  </xsl:call-template>
                </list>
              </keywords>
            </xsl:if>
            <xsl:for-each select="//text:p[@text:style-name='admotsclesital']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotsclesital']/@style:name]">
              <xsl:variable name="listOther" select="substring-after(.,': ')"/>
              <keywords scheme="keyword" xml:lang="##">
                <list>
                  <xsl:call-template name="keyWordsList">
                    <xsl:with-param name="list"><xsl:value-of select="$listOther"/></xsl:with-param>
                  </xsl:call-template>
                </list>
              </keywords>
            </xsl:for-each>
            <xsl:for-each select="//text:p[@text:style-name='admotscles_5f_inv']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles_5f_inv']/@style:name]">
              <xsl:variable name="listInv" select="substring-after(.,':')"/>
              <keywords scheme="keyword" xml:lang="##">
                <list>
                  <xsl:call-template name="InvkeyWordsList">
                    <xsl:with-param name="list"><xsl:value-of select="$listInv"/></xsl:with-param>
                  </xsl:call-template>
                </list>
              </keywords>
            </xsl:for-each>
          </textClass>
          <xsl:if test="//text:p[@text:style-name='adarcheoA-MCPactols']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adarcheoA-MCPactols']/@style:name]">
              <xsl:variable name="listPactols" select="substring-after(//text:p[@text:style-name='adarcheoA-MCPactols']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adarcheoA-MCPactols']/@style:name], ': ')"/>
              <textClass>
            	<keywords scheme="pactols">
            		<list>
            			<xsl:call-template name="keywordsPactols">
            				<xsl:with-param name="list"><xsl:value-of select="$listPactols"/></xsl:with-param>
            			</xsl:call-template>
            		</list>
            	</keywords>
              </textClass>
            </xsl:if>
        </profileDesc>
        <revisionDesc>
          <change>
            <xsl:attribute name="when">
              <xsl:apply-templates select="/office:document/office:meta/dc:date"/>
            </xsl:attribute>
            <xsl:attribute name="who">
              <xsl:apply-templates select="/office:document/office:meta/dc:creator"/>
            </xsl:attribute>
            <xsl:text>Révision</xsl:text>
          </change>
        </revisionDesc>
      </teiHeader>
    </xsl:template>

  <xsl:template match="text:variable-set|text:variable-get">
    <xsl:choose>
      <xsl:when test="contains(@text:style-name,'entitydecl')">
        <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
        <xsl:value-of select="substring-after(@text:style-name,'entitydecl_')"/>
        <xsl:text disable-output-escaping="yes">;</xsl:text>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

    <xsl:template match="text:p[@text:style-name='adauteur']" mode="header">
      <name><xsl:apply-templates/></name>
    </xsl:template>

    <xsl:template match="text:p[@text:style-name='adinstitution']" mode="header">
      <affiliation><xsl:apply-templates/></affiliation>
    </xsl:template>

	<xsl:template name="keyWordsList">
          <xsl:param name="list"/>
          <xsl:variable name="first" select="substring-before($list, ', ')" />
          <xsl:variable name="remaining" select="substring-after($list, ', ')" />
          <xsl:choose>
            <xsl:when test="$first">
              <item><xsl:value-of select="$first"/></item>
              <xsl:if test="$remaining">
                <xsl:call-template name="keyWordsList">
                  <xsl:with-param name="list" select="$remaining" />
                </xsl:call-template>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <item><xsl:value-of select="$list"/></item>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:template>

    	<xsl:template name="InvkeyWordsList">
          <xsl:param name="list"/>
          <!--xsl:variable name="first" select="substring-before($list, '،')" /-->
          <xsl:variable name="separator">
            <xsl:choose>
              <xsl:when test="contains($list,'،')">
                <xsl:text>،</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text>,</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:variable name="first" select="substring-before($list, $separator)" />
          <xsl:variable name="remaining" select="substring-after($list, $separator)" />
          <xsl:choose>
            <xsl:when test="$first">
              <item><xsl:value-of select="$first"/></item>
              <xsl:if test="$remaining">
                <xsl:call-template name="InvkeyWordsList">
                  <xsl:with-param name="list" select="$remaining" />
                </xsl:call-template>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <item><xsl:value-of select="$list"/></item>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:template>

    	<xsl:template name="keywordsPactols">
          <xsl:param name="list"/>
          <xsl:variable name="first" select="substring-before($list, ', ')" />
          <xsl:variable name="remaining" select="substring-after($list, ', ')" />
          <xsl:choose>
            <xsl:when test="$first">
              <item><xsl:value-of select="$first"/></item>
              <xsl:if test="$remaining">
                <xsl:call-template name="keywordsPactols">
                  <xsl:with-param name="list" select="$remaining" />
                </xsl:call-template>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <item><xsl:value-of select="$list"/></item>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:template>

  <xsl:template match="/office:document-content/office:body">
     <text>
<xsl:attribute name="xml:id"><xsl:text>text</xsl:text></xsl:attribute>
    <xsl:apply-templates/>
  </text>
  </xsl:template>

  <!-- sections -->
  <xsl:template match="text:h">
    <xsl:choose>
      <xsl:when test="ancestor::text:note-body">
          <xsl:apply-templates/>
      </xsl:when>
      <xsl:when test="@text:style-name='ArticleInfo'"> </xsl:when>
      <xsl:when test="@text:style-name='Abstract'">
        <div type="abstract">
          <xsl:apply-templates/>
        </div>
      </xsl:when>
      <xsl:when test="@text:style-name='Appendix'">
        <div type="appendix">
          <xsl:apply-templates/>
        </div>
      </xsl:when>
      <xsl:otherwise>
	<HEAD level="1" style="{@text:style-name}">
	  <xsl:apply-templates/>
	</HEAD>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="text:h[@text:outline-level]">
    <xsl:choose>
      <xsl:when test="ancestor::text:note-body">
        <p>
      	  <xsl:attribute name="rend">
      	    <xsl:choose>
      	      <xsl:when test="@text:style-name">
      		<xsl:value-of select="@text:style-name"/>
      	      </xsl:when>
      	      <xsl:otherwise>heading</xsl:otherwise>
      	    </xsl:choose>
      	  </xsl:attribute>
          <xsl:apply-templates/>
	      </p>
      </xsl:when>
      <!-- ajout EC 28-07-2014 -->
      <xsl:when test="@text:outline-level='1'">
      </xsl:when>
      <!-- fin ajout EC 28-07-2014 -->
      <xsl:otherwise>
	<HEAD level="{@text:outline-level}" >
	  <xsl:attribute name="style">
	    <xsl:choose>
	      <xsl:when test="@text:style-name">
		<xsl:value-of select="@text:style-name"/>
	      </xsl:when>
	      <xsl:otherwise>nostyle</xsl:otherwise>
	    </xsl:choose>
	  </xsl:attribute>
	  <xsl:apply-templates/>
	</HEAD>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- special case paragraphs -->
  <xsl:template match="text:p[@text:style-name='XMLComment']">
    <xsl:comment>
      <xsl:value-of select="."/>
    </xsl:comment>
  </xsl:template>

<xsl:template match="office:annotation/text:p">
	<note>
    	<remark>
        	<xsl:apply-templates/>
      	</remark>
    </note>
</xsl:template>

  <xsl:template match="text:p">

    <xsl:choose>
      <xsl:when test="draw:frame and parent::draw:text-box">
	<xsl:apply-templates select="draw:frame"/>
	<head>
	  <xsl:apply-templates select="text()|*[not(local-name(.)='frame')]"/>
	</head>
      </xsl:when>

      <xsl:when test="count(parent::text:note-body/text:p)=1">
          <xsl:apply-templates/>
      </xsl:when>

      <xsl:when test="count(parent::text:list-item/text:p)=1">
          <xsl:apply-templates/>
      </xsl:when>

      <xsl:when test="@text:style-name='Document Title'">
        <docTitle>
          <xsl:apply-templates/>
	</docTitle>
      </xsl:when>

      <xsl:when test="@text:style-name='Author'">
        <author>
          <xsl:apply-templates/>
        </author>
      </xsl:when>

      <xsl:when test="@text:style-name='lg'">
        <lg>
	  <xsl:for-each-group select="node()"
			      group-ending-with="text:line-break">
	    <l><xsl:apply-templates select="current-group()"/></l>
	  </xsl:for-each-group>
        </lg>
      </xsl:when>

      <xsl:when test="@text:style-name='Title'">
        <title>
          <xsl:apply-templates/>
        </title>
      </xsl:when>

      <xsl:when test="@text:style-name='Section Title'">
        <head>
          <xsl:apply-templates/>
        </head>
      </xsl:when>

      <xsl:when test="@text:style-name='Appendix Title'">
        <head>
          <xsl:apply-templates/>
        </head>
      </xsl:when>

      <xsl:when test="parent::text:list-item">
	<xsl:call-template name="applyStyle"/>
      </xsl:when>

      <xsl:when test="@text:style-name='Table'"/>

      <xsl:when test="text:span[@text:style-name = 'XrefLabel']"/>

      <xsl:when test="@text:style-name='Speech'">
        <sp>
          <speaker/>
	  <xsl:call-template name="applyStyle"/>
        </sp>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="applyStyle"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- lists -->
  <xsl:template match="text:list">
             <xsl:choose>
      <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_titre']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
    </xsl:when>
         <xsl:otherwise>
    <xsl:variable name="style">
      <xsl:for-each select="key('LISTS',@text:style-name)[1]">
	<xsl:value-of select="@text:style-name"/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:choose>
    <!-- ajout EC -->
    <xsl:when test="descendant::text:p/@text:style-name[contains(., 'puce')]">
    	<list type="unordered">
          <xsl:apply-templates/>
        </list>
    </xsl:when>
    <xsl:when test="descendant::text:p/@text:style-name[contains(., 'num')]">
    	<list type="ordered">
          <xsl:apply-templates/>
        </list>
    </xsl:when>
    <xsl:when test="descendant::text:p[@text:style-name=//office:automatic-styles/style:style[contains(@style:parent-style-name, 'num')]/@style:name]">
    	<list type="ordered">
          <xsl:apply-templates/>
        </list>
    </xsl:when>    
    <!-- fin ajout EC -->
      <xsl:when test="text:list-item/text:h">
	<xsl:for-each select="text:list-item">
	  <xsl:apply-templates/>
	</xsl:for-each>
      </xsl:when>
      <xsl:when test="@text:style-name='Var List'">
        <list>
          <xsl:apply-templates/>
        </list>
      </xsl:when>
      <xsl:when test="contains($style,'Number')">
        <list type="ordered">
          <xsl:apply-templates/>
        </list>
      </xsl:when>
      <xsl:otherwise>
        <list type="unordered">
          <xsl:apply-templates/>
        </list>
      </xsl:otherwise>
    </xsl:choose>
             </xsl:otherwise>
     </xsl:choose>
  </xsl:template>

  <xsl:template match="text:list-header">
       <xsl:choose>
      <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_titre']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
    </xsl:when>
         <xsl:otherwise>
      <head>
      <xsl:apply-templates/>
    </head>
             </xsl:otherwise>
     </xsl:choose>
  </xsl:template>

 <xsl:template match="text:list-item">
     <xsl:choose>
      <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_titre']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
    </xsl:when>
         <xsl:otherwise>
<xsl:variable name="currentStyle">
	<xsl:for-each select="descendant::text:p">
	<xsl:value-of select="@text:style-name"/>
	</xsl:for-each>
</xsl:variable>
  <xsl:variable name="listLevel">
  	<xsl:choose>
  	<!-- ajout EC 16/02/2015 -->
  		<xsl:when test="child::text:p/@text:style-name[contains(., 'puce')]">
  			<xsl:value-of select="substring-after(child::text:p/@text:style-name,'puce')"/>
  		</xsl:when>
  		<xsl:when test="child::text:p/@text:style-name[contains(., 'num')]">
  			<xsl:value-of select="substring-after(child::text:p/@text:style-name,'num')"/>
  		</xsl:when>
		<xsl:when test="child::text:p[@text:style-name=//style:style[contains(@style:parent-style-name,'puce')]/@style:name]">
			<xsl:value-of select="substring-after($OOstyles//style:style[@style:name=$currentStyle]/@style:parent-style-name,'puce')"/>
		</xsl:when>
		<xsl:when test="child::text:p[@text:style-name=//style:style[contains(@style:parent-style-name,'num')]/@style:name]">
			<xsl:value-of select="substring-after($OOstyles//style:style[@style:name=$currentStyle]/@style:parent-style-name,'num')"/>
		</xsl:when>
  	<!-- fin ajout EC -->
  		<xsl:otherwise>
  			<xsl:value-of select="substring-after(../@text:style-name,'Numbering_20_')"/>
  		</xsl:otherwise>
  	</xsl:choose>
  </xsl:variable>
  <xsl:variable name="styleListe">
    <xsl:choose>
      <xsl:when test="text:p[starts-with(@text:style-name,'adFocusListe')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adFocusListe')]/@style:name]"><xsl:text>txt_Focus_Liste_</xsl:text><xsl:value-of select="$listLevel"/></xsl:when>
      <xsl:otherwise><xsl:text>txt_Liste_</xsl:text><xsl:value-of select="$listLevel"/></xsl:otherwise>
    </xsl:choose>
</xsl:variable>
	<xsl:choose>
    	<xsl:when test="parent::text:list/@text:style-name='Var List'">
      		<item>
        		<xsl:for-each select="text:p[@text:style-name='VarList Term']">
          			<xsl:apply-templates select="."/>
        		</xsl:for-each>
      		</item>
    	</xsl:when>
    	<xsl:otherwise>
          <item style="{$styleListe}">
        		<xsl:apply-templates/>
      		</item>
    	</xsl:otherwise>
  	</xsl:choose>
                </xsl:otherwise>
     </xsl:choose>
</xsl:template>

  <xsl:template
    match="text:p[@text:style-name='VarList Item' or
	   @text:style-name='List Contents']">
    <GLOSS n="item">
      <xsl:apply-templates/>
    </GLOSS>
  </xsl:template>

  <xsl:template
    match="text:p[@text:style-name='VarList Term' or @text:style-name='List Heading']">
    <GLOSS n="label">
      <xsl:apply-templates/>
    </GLOSS>
  </xsl:template>

<xsl:template match="text:p[@text:style-name='VarList Item' or @text:style-name='List Contents']">
    <xsl:if test="not(preceding-sibling::text:p[@text:style-name='VarList Item'])">
      <xsl:text disable-output-escaping="yes">&lt;item&gt;</xsl:text>
    </xsl:if>
    <xsl:apply-templates/>
    <xsl:if test="not(following-sibling::text:p[@text:style-name='VarList Item'])">
      <xsl:text disable-output-escaping="yes">&lt;/item&gt;</xsl:text>
    </xsl:if>
  <xsl:variable name="next">
    <xsl:for-each select="following-sibling::text:p[1]">
        <xsl:value-of select="@text:style-name"/>
    </xsl:for-each>
  </xsl:variable>
<xsl:choose>
    <xsl:when test="$next='VarList Term'"/>
    <xsl:when test="$next='List Heading'"/>
    <xsl:when test="$next='VarList Item'"/>
    <xsl:when test="$next='List Contents'"/>
    <xsl:otherwise>
      <xsl:text disable-output-escaping="yes">&lt;/list&gt;</xsl:text>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='VarList Term' or @text:style-name='List Heading']">
	<xsl:variable name="prev">
    	<xsl:for-each select="preceding-sibling::text:p[1]">
        	<xsl:value-of select="@text:style-name"/>
    	</xsl:for-each>
  	</xsl:variable>
  	<xsl:choose>
    	<xsl:when test="$prev='VarList Term'"/>
    	<xsl:when test="$prev='List Heading'"/>
    	<xsl:when test="$prev='VarList Item'"/>
    	<xsl:when test="$prev='List Contents'"/>
    	<xsl:otherwise>
        	<xsl:text disable-output-escaping="yes">&lt;list type="gloss"&gt;</xsl:text>
    	</xsl:otherwise>
  	</xsl:choose>
    <label>
    	<xsl:apply-templates/>
    </label>
</xsl:template>


<xsl:template match="text:p[@text:style-name='adadresse']">
	<p style="Auteur_Adresse">
		<xsl:apply-templates/>
	</p>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcellule']">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcitationital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcitationital']/@style:name]">
	<xsl:choose>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
		</xsl:when>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
		</xsl:when>
		<xsl:otherwise>
			<quote style="txt_Citation" rend="quotation italique">
			<xsl:apply-templates/>
            <xsl:if test="following-sibling::text:p[1][@text:style-name='adsources']">
                <xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adsources']" mode="inQuote"/>
            </xsl:if>
		</quote>
		</xsl:otherwise>
	</xsl:choose>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcitationrom']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcitationrom']/@style:name]">
	<xsl:choose>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name='Titre-recension']">
		</xsl:when>
    <xsl:when test="preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
		</xsl:when>
		<xsl:otherwise>
			<quote style="txt_Citation" rend="quotation">
				<xsl:apply-templates/>
                <xsl:if test="following-sibling::text:p[1][@text:style-name='adsources']">
                    <xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adsources']" mode="inQuote"/>
                </xsl:if>
			</quote>
		</xsl:otherwise>
	</xsl:choose>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>



				<!--test pour adcit_5f_inv-->
<xsl:template match="text:p[@text:style-name='adcit_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcit_5f_inv']/@style:name]">
  <xsl:variable name="readOrder">
    <xsl:choose>
      <xsl:when test="//office:automatic-styles/style:style[@style:name='adcit_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
        <xsl:text>rtl</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ltr</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
	<quote style="txt_Citation_inv" rend="{$readOrder}">
		<xsl:apply-templates/>
	</quote>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<!-- adCA_5f_inv styles de caractères inverse -->
<xsl:template match="text:span[@text:style-name='adCA_5f_inv']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCA_5f_inv']/@style:name]">
  <xsl:variable name="readOrder">
    <!--xsl:choose>
      <xsl:when test="//office:automatic-styles/style:style[@style:name='adCA_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
        <xsl:text>rtl</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ltr</xsl:text>
      </xsl:otherwise>
    </xsl:choose-->
  </xsl:variable>
	<hi style="typo_inv" rend="rtl">
		<xsl:apply-templates/>
	</hi>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[@text:style-name='addefinition']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addefinition']/@style:name]">
  <p><gloss style="txt_Definition">
		<xsl:apply-templates/>
              </gloss></p>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[starts-with(@text:style-name,'adlocal')][not(parent::text:note-body)]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adlocal')]/@style:name][not(parent::text:note-body)]">
  <xsl:variable name="style">
    <xsl:choose>
      <xsl:when test="starts-with(@text:style-name,'P')">
        <xsl:value-of select="//office:automatic-styles/style:style[@style:parent-style-name=@text:style-name]"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="@text:style-name"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <p style="{$style}">
    <xsl:apply-templates/>
  </p>
  <!--  <xsl:text disable-output-escaping="yes">
  </xsl:text> -->
</xsl:template>

<!-- adlocal caracteres -->
<xsl:template match="text:span[starts-with(@text:style-name,'adlocal')]|text:span[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adlocal')]/@style:name]">
	<xsl:variable name="carstyle">
		<xsl:choose>
			<xsl:when test="starts-with(@text:style-name,'T')">
				<xsl:value-of select="//office:automatic-styles/style:style[@style:parent-style-name=@text:style-name]"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="@text:style-name"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
		<hi style="typo_{$carstyle}">
			<xsl:apply-templates/>
		</hi>
	<!--<xsl:text disable-output-escaping="yes"></xsl:text>-->
</xsl:template>

<!-- <xsl:template match="text:p[@text:style-name='adFocus']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adFocus']/@style:name]">
	<p style="txt_Focus" rend="focus">
		<xsl:apply-templates/>
	</p>
	<xsl:text disable-output-escaping="yes">
	</xsl:text>
</xsl:template> -->

<xsl:template match="text:p[@text:style-name='adTFocus']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTFocus']/@style:name]">
	<p style="T_Focus" rend="focus">
		<xsl:apply-templates/>
	</p>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcitationital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcitationital']/@style:name]">
	<quote style="txt_Citation_italique" rend="quotation italique">
		<xsl:apply-templates/>
        <xsl:if test="following-sibling::text:p[1][@text:style-name='adsources']">
            <xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adsources']" mode="inQuote"/>
        </xsl:if>
	</quote>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<xsl:template match="text:p[@text:style-name='adseparateur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adseparateur']/@style:name]">
    <xsl:choose>
        <xsl:when test="not(string(.))">
            <xsl:element name="tei:p">
                <xsl:attribute name="rend">break</xsl:attribute>
                <xsl:attribute name="style">txt_separateur</xsl:attribute>
                <xsl:text> </xsl:text>
            </xsl:element>
        </xsl:when>
        <xsl:otherwise>
            <p rend="break" style="txt_separateur">
                <xsl:apply-templates/>
		    </p>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcode']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcode']/@style:name]">
	<p><code style="txt_code">
		<xsl:apply-templates/>
	</code></p>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adquestion']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adquestion']/@style:name]">
	<sp>
	 <xsl:if test="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]">
		<xsl:attribute name="who"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></xsl:attribute>
		<speaker style="typo_loc"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></speaker>
	 </xsl:if>
	<p rend="question" style="txt_question">
		<xsl:apply-templates/>
	</p>
	</sp>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adreponse']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adreponse']/@style:name]">
	<sp>
	  <xsl:if test="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]">
		<xsl:attribute name="who"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></xsl:attribute>
		<speaker style="typo_loc"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></speaker>
	  </xsl:if>
	<p rend="answer" style="txt_reponse">
		<xsl:apply-templates/>
	</p>
	</sp>
</xsl:template>

<!-- linguistique -->
<xsl:template match="//text:p[@text:style-name='adexemple']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexemple']/@style:name]">
	<quote type="exemple">
		<quote>
		<xsl:choose>
			<xsl:when test="text:span[@text:style-name='adCAnum']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnum']/@style:name]">
				<num><xsl:value-of select="text:span[@text:style-name='adCAnum']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnum']/@style:name]"/></num>
				<seg><xsl:apply-templates/></seg>
			</xsl:when>
			<xsl:otherwise>
				<seg><xsl:apply-templates/></seg>
			</xsl:otherwise>
		</xsl:choose>
		</quote>
		<xsl:if test="following-sibling::text:p[1][@text:style-name='adexempletrad']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempletrad']/@style:name]">
			<quote>
				<seg>
					<xsl:value-of select="following::text:p[1][@text:style-name='adexempletrad']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempletrad']/@style:name]"/>
				</seg>
			</quote>
			<xsl:choose>
				<xsl:when test="following::text:p[2][@text:style-name='adglose']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adglose']/@style:name]">
					<quote type="glose">
						<xsl:value-of select="following::text:p[2][@text:style-name='adglose']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adglose']/@style:name]"/>
					</quote>
					<xsl:choose>
						<xsl:when test="following::text:p[3][@text:style-name='adglose']|following-sibling::text:p[3][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adglose']/@style:name]">
							<quote type="glose">
								<xsl:value-of select="following::text:p[3][@text:style-name='adglose']|following-sibling::text:p[3][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adglose']/@style:name]"/>
							</quote>
							<xsl:choose>
								<xsl:when test="following::text:p[4][@text:style-name='adexempleref']|following-sibling::text:p[4][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]">
									<bibl style="txt_Biblio">
										<xsl:value-of select="following::text:p[4][@text:style-name='adexempleref']|following-sibling::text:p[4][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]"/>
									</bibl>
								</xsl:when>
							</xsl:choose>
						</xsl:when>
						<xsl:when test="following::text:p[3][@text:style-name='adexempleref']|following-sibling::text:p[3][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]">
							<bibl style="txt_Biblio">
									<xsl:value-of select="following::text:p[3][@text:style-name='adexempleref']|following-sibling::text:p[3][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]"/>
							</bibl>
						</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="following::text:p[2][@text:style-name='adexempleref']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]">
					<bibl style="txt_Biblio">
							<xsl:value-of select="following::text:p[2][@text:style-name='adexempleref']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]"/>
					</bibl>
				</xsl:when>
			</xsl:choose>
		</xsl:if>
	</quote>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adglose']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adglose']/@style:name]"/>

<xsl:template match="text:p[@text:style-name='adexempletrad']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempletrad']/@style:name]"/>

<xsl:template match="text:p[@text:style-name='adexempleref']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adexempleref']/@style:name]"/>

<xsl:template match="text:p[@text:style-name='Standard']|text:p[@text:style-name='puctexte']|text:p[@text:style-name='Normal']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name]">
	<xsl:choose>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']|preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
		</xsl:when>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='Titre-recension']|preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
		</xsl:when>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
		</xsl:when>
		<xsl:otherwise>
			<p style="txt_Normal">
      			<xsl:apply-templates/>
    		</p>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adcontinued-para']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name]">
	<xsl:choose>
    <xsl:when test="preceding::text:p[starts-with(@text:style-name,'Titre-recension')]|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
    </xsl:when>
        <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
    </xsl:when>
        <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_titre']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    </xsl:when>
        <xsl:otherwise>
    <p style="txt_Normal_suite">
      	<xsl:apply-templates/>
    </p>
            </xsl:otherwise>
    </xsl:choose>
</xsl:template>

				<!--test pour adtexte_5f_inv-->
<xsl:template match="text:p[@text:style-name='adtexte_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtexte_5f_inv']/@style:name]">
  <xsl:variable name="readOrder">
    <xsl:choose>
      <xsl:when test="//office:automatic-styles/style:style[@style:name='adtexte_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
        <xsl:text>rtl</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ltr</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
	<p style="txt_Normal_inv" rend="{$readOrder}">
		<xsl:apply-templates/>
	</p>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:template>

<!--<xsl:template match="text:p[@text:style-name='adannexe']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adannexe']/@style:name]"/>-->

<!-- Annexe dans le back -->
<xsl:template name="annexeBack">
	<div type="annexe">
		<head style="T_1">
			<xsl:apply-templates select="text:p[@text:style-name='Titre-section-annexe']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-annexe']/@style:name]"/>
		</head>
		<xsl:for-each select="text:p[@text:style-name='adinclusion'][preceding-sibling::text:p[@text:style-name='Titre-section-annexe']]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinclusion']/@style:name][preceding-sibling::text:p[@text:style-name='Titre-section-annexe']]">
			<floatingText type="annexe">
				<group>
					<xi:include>
						<xsl:attribute name="href"><xsl:value-of select="concat(.,'.xml')"/></xsl:attribute>
						<xsl:attribute name="xpointer"><xsl:text>text</xsl:text></xsl:attribute>
					</xi:include>
				</group>
			</floatingText>
		</xsl:for-each>
	</div>
</xsl:template>

<xsl:template match="text:p[@text:outline-level][preceding-sibling::text:p[@text:style-name='Titre-section-annexe']]"/>

<!-- Fin de l'annexe dans le back -->

  <!-- inline -->

  <xsl:template match="text:span">
    <xsl:variable name="Style">
      <xsl:value-of select="@text:style-name"/>
    </xsl:variable>
    <xsl:choose>
      <xsl:when test="$Style='Emphasis'">
        <hi rend="italic" style="typo_Italique">
          <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='Underline'">
        <hi rend="underline">
          <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='Strong_20_Emphasis'">
          <xsl:apply-templates/>
      </xsl:when>
      <xsl:when test="$Style='SmallCaps'">
        <hi rend="sc">
          <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='adCAnum'"></xsl:when>
      <xsl:when test="$Style='adCAnumill'">
      	<hi style="typo_numill">
      		<xsl:apply-templates/>
      	</hi>
      </xsl:when>
      <xsl:when test="$Style='adCAlocuteur'"></xsl:when>
      <xsl:when test="$Style='adCAsources'">
        <bibl style="typo_sources" rend="inline">
          <xsl:apply-templates/>
        </bibl>
      </xsl:when>
      <xsl:when test="$Style='adCAcredits'">
        <desc style="typo_credits">
          <xsl:apply-templates/>
        </desc>
      </xsl:when>
      <xsl:when test="$Style='adCAcitation'">
        <quote style="typo_citation">
          <xsl:apply-templates/>
        </quote>
      </xsl:when>
      <xsl:when test="$Style='Emphasis Bold'">
        <hi rend="bold">
          <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='Highlight'">
        <hi>
          <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='q'">
        <q>
          <xsl:choose>
            <xsl:when test="starts-with(.,'&#x2018;')">
              <xsl:value-of
                select="substring-before(substring-after(.,'&#x2018;'),'&#x2019;')"
              />
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates/>
            </xsl:otherwise>
          </xsl:choose>
        </q>
      </xsl:when>
      <xsl:when test="$Style='Internet Link'">
        <xsl:apply-templates/>
      </xsl:when>
      <xsl:when test="$Style='SubScript'">
	<hi rend="sub">
	  <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="$Style='date'">
        	<date>
          		<xsl:apply-templates/>
        	</date>
      	</xsl:when>
      <xsl:when test="$Style='SuperScript'">
        <hi rend="sup">
	  <xsl:apply-templates/>
        </hi>
      </xsl:when>
      <xsl:when test="style:text-properties[@fo:text-transform='small-caps']">
	<hi rend="sc">
	  <xsl:apply-templates/>
	</hi>
      </xsl:when>
      <xsl:when test="../text:h">
        <xsl:apply-templates/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="applyStyle"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

<xsl:template name="applyStyle">
	<xsl:variable name="name">
    	<xsl:value-of select="@text:style-name"/>
  	</xsl:variable>
 	<xsl:choose>
   		<xsl:when test="key('STYLES',$name)">
     		<xsl:variable name="contents">
       			<xsl:apply-templates/>
     		</xsl:variable>
     		<xsl:for-each select="key('STYLES',$name)">
<!--
    <xsl:message>! <xsl:for-each select="style:text-properties/@*">
    <xsl:value-of select="name(.)"/>:        <xsl:value-of select="."/>&#10;
    </xsl:for-each>
    </xsl:message>
-->
       			<xsl:choose>	 	<!--ajouté d'après syntaxe-->
              <xsl:when test="style:text-properties[@fo:font-weight='bold'] and style:text-properties[@fo:font-style='italic'] and style:text-properties[starts-with(@style:text-position,'super')]">
                  <hi rend="sup italic bold" style="typo_exposant_italic_gras" >
                    <xsl:copy-of select="$contents"/>
                  </hi>
                </xsl:when>
          <xsl:when test="style:text-properties[@fo:font-style='italic'] and style:text-properties[@fo:font-weight='bold']">
     				<hi rend="italic bold" style="typo_italic_gras" >
     					<xsl:copy-of select="$contents"/>
     				</hi>
     			</xsl:when>
				<xsl:when test="style:text-properties[@fo:font-style='italic'] and style:text-properties[@fo:font-variant='small-caps']">
     				<hi rend="small-caps italic" style="typo_SC_italic" >
     					<xsl:copy-of select="$contents"/>
     				</hi>
     			</xsl:when>
          <xsl:when test="style:text-properties[@fo:font-weight='bold'] and style:text-properties[@fo:font-variant='small-caps']">
       				<hi rend="small-caps bold" style="typo_SC_bold" >
       					<xsl:copy-of select="$contents"/>
       				</hi>
       			</xsl:when>
          <xsl:when test="style:text-properties[@fo:font-style='italic' and starts-with(@style:text-underline-style,'s')]">
              <hi rend="italic underline" style="typo_italic_souligne" >
                <xsl:copy-of select="$contents"/>
              </hi>
            </xsl:when>
				<xsl:when test="style:text-properties[starts-with(@style:text-position,'-')]">
						<xsl:choose>
							<xsl:when test="style:text-properties[starts-with(@fo:font-variant,'small')]">
	   							<hi rend="sub-small-caps" style="typo_SC_Indice" >
	     							<xsl:copy-of select="$contents"/>
	   							</hi>
							</xsl:when>
							<xsl:otherwise>
	   							<hi style="typo_Indice" rend="sub">
	     							<xsl:copy-of select="$contents"/>
	   							</hi>
							</xsl:otherwise>
						</xsl:choose>
				</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@fo:font-variant,'small')]">
              <hi rend="small-caps" style="typo_SC" >
	    				<xsl:copy-of select="$contents"/>
	   				</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@style:text-position,'super')]">
					<xsl:choose>
	     				<xsl:when  test="style:text-properties[@fo:font-style='italic']">
	       					<hi style="typo_Exposant_Italic" rend="sup italic">
	         					<xsl:copy-of select="$contents"/>
	       					</hi>
	     				</xsl:when>
	     				<xsl:otherwise>
	     					<xsl:choose>
	     						<xsl:when test="contains($name,'note')">
	     							<xsl:copy-of select="$contents"/>
	     						</xsl:when>
	     						<xsl:otherwise>
		     						<hi style="typo_Exposant" rend="sup">
			         					<xsl:copy-of select="$contents"/>
			        				</hi>
			    				</xsl:otherwise>
							</xsl:choose>
	     				</xsl:otherwise>
	     			</xsl:choose>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@style:text-underline-style,'s')]">
				   <hi style="typo_souligne" rend="underline">
	     				<xsl:copy-of select="$contents"/>
	   				</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@fo:text-transform,'upper')]">
				   	<hi style="typo_Majuscule" rend="capitale">
	    				<xsl:copy-of select="$contents"/>
	 				</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@style:text-position,'sub')]">
	 				<xsl:choose>
	 					<xsl:when test="style:text-properties[@fo:font-style='italic']">
	 						<hi style="typo_Indice_Italique" rend="sub italic">
	     						<xsl:copy-of select="$contents"/>
	   						</hi>
	 					</xsl:when>
	 					<xsl:otherwise>
	   				<hi style="typo_Indice" rend="sub">
	     				<xsl:copy-of select="$contents"/>
	   				</hi>
	 					</xsl:otherwise>
	 				</xsl:choose>
	 			</xsl:when>
     			<xsl:when test="style:text-properties[@fo:font-weight='bold']">
	   					<hi rend="bold" style="typo_gras">
	     					<xsl:copy-of select="$contents"/>
	   					</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[@style:text-line-through-style='solid']">
	   				<hi style="typo_line-through" rend="line-through">
	     				<xsl:copy-of select="$contents"/>
	   				</hi>
	 			</xsl:when>
				<xsl:when test="style:text-properties[@style:text-underline-type='double']">
	   					<hi rend="double-underline" style="typo_dble_souligne">
	     					<xsl:copy-of select="$contents"/>
	   					</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[@style:text-underline='single']">
	   				<hi style="typo_souligne" rend="underline">
	     				<xsl:copy-of select="$contents"/>
	   				</hi>
	 			</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@fo:font-style,'ita')]">
	   				<hi rend="italic" style="typo_Italique">
						<xsl:copy-of select="$contents"/>
	   				</hi>
				</xsl:when>
	 			<xsl:when test="style:text-properties[starts-with(@fo:font-style,'norm')]">
	   				<hi rend="italic" style="typo_Italique">
				    	<xsl:copy-of select="$contents"/>
	   				</hi>
				</xsl:when>
					<!-- test récupération des langues
				<xsl:when test="style:text-properties[@fo:language]">
	   				<hi>
	   					<xsl:attribute name="xml:lang">
	   						<xsl:value-of select="style:text-properties/@fo:language"/>
	   					</xsl:attribute>
				    	<xsl:copy-of select="$contents"/>
	   				</hi>
				</xsl:when>	 -->
	 			<xsl:when test="@style:parent-style-name='adresume'">
					<p style="txt_Resume" xml:lang="##">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
	 			<xsl:when test="@style:parent-style-name='adresumeital'">
					<p style="txt_Resume_italique" xml:lang="##">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
                <xsl:when test="@style:parent-style-name='adchapo'">
					<p style="txt_chapo">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>    
 	 			<xsl:when test="@style:parent-style-name='admail'">
					<p style="auteur_Courriel">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='TitreTraduit'">
					<head style="T_0_Article_UK">
						<xsl:copy-of select="$contents"/>
					</head>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adinstitution'">
					<byline style="auteur_Institution">
						<xsl:copy-of select="$contents"/>
					</byline>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adadresse'">
					<p style="Auteur_Adresse">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='admotscles'">
					<p style="txt_Motclef">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='admotsclesital'">
					<p style="txt_Keywords">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
	 			<xsl:when test="@style:parent-style-name='admotscles_5f_inv'">
					<p rend="rtl" style="txt_motscles_inv">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adcitationrom'">
					<quote style="txt_Citation" rend="quotation">
						<xsl:copy-of select="$contents"/>
					</quote>
	 			</xsl:when>
				<xsl:when test="@style:parent-style-name='adcitationital'">
					<quote style="txt_Citation_italique" rend="quotation italique">
						<xsl:copy-of select="$contents"/>
					</quote>
	 			</xsl:when>
								<!--intégration des styles inversés -->
				<xsl:when test="@style:parent-style-name='adcit_5f_inv'">
                                  <xsl:variable name="readOrder">
                                    <xsl:choose>
                                      <xsl:when test="//office:automatic-styles/style:style[@style:name='adcit_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
                                        <xsl:text>rtl</xsl:text>
                                      </xsl:when>
                                      <xsl:otherwise>
                                        <xsl:text>ltr</xsl:text>
                                      </xsl:otherwise>
                                    </xsl:choose>
                                  </xsl:variable>
					<quote style="txt_Citation_inv" rend="{$readOrder}">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>
				<xsl:when test="@style:parent-style-name='adtexte_5f_inv'">
                                  <xsl:variable name="readOrder">
                                    <xsl:choose>
                                      <xsl:when test="//office:automatic-styles/style:style[@style:name='adcit_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
                                        <xsl:text>rtl</xsl:text>
                                      </xsl:when>
                                      <xsl:otherwise>
                                        <xsl:text>ltr</xsl:text>
                                      </xsl:otherwise>
                                    </xsl:choose>
                                  </xsl:variable>
					<p style="txt_Normal_inv" rend="{$readOrder}">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
				<!--xsl:when test="@style:parent-style-name='adtitre_5f_inv'">
                                  <xsl:variable name="readOrder">
                                    <xsl:choose>
                                      <xsl:when test="//office:automatic-styles/style:style[@style:name='adtitre_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
                                        <xsl:text>rtl</xsl:text>
                                      </xsl:when>
                                      <xsl:otherwise>
                                        <xsl:text>ltr</xsl:text>
                                      </xsl:otherwise>
                                    </xsl:choose>
                                  </xsl:variable>
					<head style="T_inv" rend="{$readOrder}">
						<xsl:apply-templates/>
					</head>
				</xsl:when>
				<xsl:when test="@style:parent-style-name='adresume_5f_inv'">
                                  <xsl:variable name="readOrder">
                                    <xsl:choose>
                                      <xsl:when test="//office:automatic-styles/style:style[@style:name='adresume_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
                                        <xsl:text>rtl</xsl:text>
                                      </xsl:when>
                                      <xsl:otherwise>
                                        <xsl:text>ltr</xsl:text>
                                      </xsl:otherwise>
                                    </xsl:choose>
                                  </xsl:variable>
					<p style="txt_resume_inv" rend="{$readOrder}">
						<xsl:apply-templates/>
					</p>
				</xsl:when-->
                                <!-- <xsl:when test="@style:parent-style-name='adexemple'">
					<quote>
						<xsl:copy-of select="$contents"/>
					</quote>
	 			</xsl:when>
	  	 		<xsl:when test="@style:parent-style-name='adexempleref'">
					<bibl>
						<xsl:copy-of select="$contents"/>
					</bibl>
	 			</xsl:when> -->
 	 			<xsl:when test="@style:parent-style-name='Standard'">
					<p style="txt_Normal">
						<xsl:copy-of select="$contents"/>
					</p>
					<!--<xsl:text disable-output-escaping="yes">
					</xsl:text>-->
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='Normal'">
					<p style="txt_Normal">
						<xsl:copy-of select="$contents"/>
					</p>
					<!--<xsl:text disable-output-escaping="yes">
					</xsl:text>-->
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adannexe'">
					<p style="txt_Annexe">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adcellule'">
                                  <xsl:copy-of select="$contents"/>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adTitrePartie'">
					<p style="T_2_Partie">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adauteur'">
					<p style="auteur">
						<xsl:copy-of select="$contents"/>
					</p>
	 			</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adbiblio'">
					<p style="txt_Bibliographie">
						<xsl:copy-of select="$contents"/>
					</p>
				</xsl:when>
 	 			<xsl:when test="@style:parent-style-name='adCAnum'">
				</xsl:when>
				<xsl:when test="@style:parent-style-name='adCAlocuteur'"></xsl:when>
				<xsl:when test="@style:parent-style-name='adCA_5f_inv'">
				</xsl:when>
	 			<xsl:otherwise>
					<xsl:copy-of select="$contents"/>
    			</xsl:otherwise>
     			</xsl:choose>
     		</xsl:for-each>
   		</xsl:when>
   		<xsl:otherwise>
     		<xsl:apply-templates/>
   		</xsl:otherwise>
 	</xsl:choose>
 </xsl:template>

<!-- neutral 
<xsl:template match="text:span[@text:style-name='adCAneutral']">
  <hi rendition="neutral"><xsl:apply-templates/></hi>
</xsl:template>
-->

  <!-- notes -->
  <xsl:template match="text:note-citation"/>

  <xsl:template match="text:note-body">
  	<xsl:apply-templates/>
  </xsl:template>
  
  <!-- éviter indentation à cause de nœuds texte dans les notes -->
  <xsl:template match="text:note-body/text()"/>

	<xsl:template match="text:note-body/text:p">
    <p><xsl:apply-templates/></p>
	</xsl:template>

<!-- NDLR adlocal
<xsl:template match="text:note">
  <note>
  <xsl:attribute name="style">txt_Note</xsl:attribute>
  <xsl:attribute name="type">standard</xsl:attribute>
  <xsl:attribute name="xml:id">
  	<xsl:value-of select="@text:id"/>
  </xsl:attribute>
    <xsl:choose>

      <xsl:when test="text:note-body/text:p/@text:style-name='Footnote'">
        <xsl:attribute name="type">standard</xsl:attribute>
        <xsl:attribute name="place">foot</xsl:attribute>
      </xsl:when>

      <xsl:when test="text:note-body/text:p/starts-with(@text:style-name,'adlocal')">
      	<xsl:variable name="NotesAdlocal" select="substring-after(text:note-body/text:p/@text:style-name,'adlocal')">
        </xsl:variable>
        <xsl:attribute name="type"><xsl:value-of select="$NotesAdlocal"/></xsl:attribute>
      </xsl:when>
    </xsl:choose>
	  <xsl:choose>
      <xsl:when test="@text:note-class='endnote'">
        <xsl:attribute name="place">end</xsl:attribute>
        <xsl:attribute name="n"><xsl:value-of select="./text:note-citation/@text:label"/></xsl:attribute>
      </xsl:when>
      <xsl:otherwise>
      	  <xsl:attribute name="n"><xsl:value-of select="./text:note-citation"/></xsl:attribute>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
		<xsl:when test="text:note-body/text:p[@text:style-name='adnote_5f_inv']">
			<xsl:attribute name="style">txt_Note_inv</xsl:attribute>
			<xsl:attribute name="rend">rtl</xsl:attribute>
		</xsl:when>
		<xsl:otherwise>
			<xsl:attribute name="style">txt_Note</xsl:attribute>
		</xsl:otherwise>
    </xsl:choose>
			<xsl:apply-templates/>
		</note>
</xsl:template> -->

<!-- Notes-->
<xsl:template match="text:note">
  <note>
    <xsl:attribute name="style">txt_Note</xsl:attribute>
  	<xsl:attribute name="xml:id">
  		<xsl:value-of select="@text:id"/>
  	</xsl:attribute>
  	<xsl:attribute name="place">
    	<xsl:choose>
    		<xsl:when test="@text:note-class='endnote'">
    			<xsl:attribute name="place">end</xsl:attribute>
    		</xsl:when>
    		<xsl:when test="@text:note-class='footnote'">
    			<xsl:attribute name="place">foot</xsl:attribute>
    		</xsl:when>
    	</xsl:choose>
    </xsl:attribute>
  	<xsl:attribute name="n">
  		<xsl:value-of select="text:note-citation"/>
  	</xsl:attribute>
  	<xsl:choose>
  		<xsl:when test="descendant::text:p[starts-with(@text:style-name,'adlocal')]">
  		<xsl:variable name="LocalNote" select="descendant::text:p/@text:style-name"/>
  			<xsl:attribute name="type">
  				<xsl:value-of select="substring-after($LocalNote,'adlocal')"/>
  			</xsl:attribute>
  		</xsl:when>
        <xsl:when test="starts-with(descendant::text:p[1]/@text:style-name,'P')">
            <xsl:variable name="shortcutStyleName">
                <xsl:value-of select="descendant::text:p/@text:style-name"/>
            </xsl:variable>
            <xsl:variable name="trueStyleName">
                <xsl:value-of select="preceding::office:automatic-styles/style:style[@style:name=$shortcutStyleName]/@style:parent-style-name"/>
            </xsl:variable>
  			<xsl:attribute name="type">
                <xsl:choose>
                    <xsl:when test="contains($trueStyleName,'adlocal')">
                        <xsl:value-of select="substring-after($trueStyleName,'adlocal')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>standard</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
  			</xsl:attribute>
  		</xsl:when>
  		<xsl:otherwise>
  			<xsl:attribute name="type">standard</xsl:attribute>
  		</xsl:otherwise>
  	</xsl:choose>
	<xsl:apply-templates/>
</note>
</xsl:template>

  <xsl:template match="text:note-ref">
    <ref target="#{@text:ref-name}">
      <xsl:apply-templates/>
    </ref>
  </xsl:template>

<!--  <xsl:template match="text:note">
    <note>
      <xsl:if test="@text:id">
	<xsl:attribute name="xml:id">
	  <xsl:value-of select="@text:id"/>
	</xsl:attribute>
      </xsl:if>
      <xsl:choose>
        <xsl:when test="@text:note-class='endnote'">
          <xsl:attribute name="place">end</xsl:attribute>
        </xsl:when>
        <xsl:when test="@text:note-class='footnote'">
          <xsl:attribute name="place">foot</xsl:attribute>
        </xsl:when>
      </xsl:choose>
      <xsl:if test="text:note-citation">
	<xsl:attribute name="n">
	  <xsl:value-of select="text:note-citation"/>
	</xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </note>
  </xsl:template> -->

  <!-- linking -->
  <xsl:template match="text:a">
    <xsl:choose>
      <xsl:when test="starts-with(@xlink:href,'mailto:')">
        <xsl:choose>
          <xsl:when test=".=@xlink:href">
            <ptr target="{substring-after(@xlink:href,'mailto:')}"/>
            <xsl:apply-templates/>
          </xsl:when>
          <xsl:otherwise>
            <ref target="{@xlink:href}">
              <xsl:apply-templates/>
            </ref>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <!-- commenté EC fév 2015
      <xsl:when test="contains(@xlink:href,'://')">
        <xsl:choose>
          <xsl:when test=".=@xlink:href">
            <ptr target="{@xlink:href}"/>
          </xsl:when>
          <xsl:otherwise>
            <ref target="{@xlink:href}">
              <xsl:apply-templates/>
            </ref>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>-->
      <xsl:when test="not(contains(@xlink:href,'#'))">
        <ref target="{@xlink:href}">
          <xsl:apply-templates/>
        </ref>
      </xsl:when>
     <!-- récupération du bon chemin pour les références croisées entre deux documents-->
      <xsl:when test="contains(@xlink:href,'styles')">
      	<xsl:variable name="refext" select="substring-after(substring-before(@xlink:href,'.d'),'s/')"/>
      	<xsl:variable name="refid" select="substring-after(@xlink:href,'#')"/>
      	<ref type="crossref">
      	<xsl:attribute name="target">
			<xsl:value-of select="concat($refext,'.xml#',$refid)"/>
      	</xsl:attribute>
              <xsl:apply-templates/>
        </ref>
      </xsl:when>
      <xsl:when test="contains(@xlink:href,'#')">
      	<xsl:variable name="internLinkRef"><xsl:value-of select="substring-after(@xlink:href,'#')"/></xsl:variable>
        <ref>
        	<xsl:attribute name="target">
        		<xsl:value-of select="concat('#',$internLinkRef)"/>
        	</xsl:attribute>
          <xsl:apply-templates/>
        </ref>
      </xsl:when>

      <xsl:otherwise>
        <xsl:variable name="linkvar" select="@xlink:href"/>
        <xsl:choose>
          <xsl:when test=".=$linkvar">
            <ptr target="{$linkvar}"/>
          </xsl:when>
          <xsl:otherwise>
            <ref target="{$linkvar}">
              <xsl:apply-templates/>
            </ref>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="text:line-break">
    <xsl:choose>
      <xsl:when test="parent::text:span[@text:style-name='l']"/>
      <xsl:when test="parent::text:p[@text:style-name='lg']"/>
      <xsl:otherwise>
	<lb/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="text:tab">
    <xsl:text>	</xsl:text>
  </xsl:template>

  <xsl:template match="text:reference-ref">
    <ptr target="#{@text:ref-name}"/>
  </xsl:template>

  <xsl:template name="id.attribute.literal">
    <xsl:if test="child::text:reference-mark-start">
      <xsl:text> xml:id=&quot;</xsl:text>
	<!--xsl:text>id_</xsl:text-->
        <xsl:value-of select="child::text:reference-mark-start/@text:style-name"
        />
	<xsl:text>&quot;</xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template name="id.attribute">
    <xsl:if test="child::text:reference-mark-start">
      <xsl:attribute name="xml:id">
	<!--xsl:text>id_</xsl:text-->
        <xsl:value-of select="child::text:reference-mark-start/@text:style-name"
        />
      </xsl:attribute>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text:reference-mark-start"/>

  <xsl:template match="text:reference-mark-end"/>

  <xsl:template match="comment">
    <xsl:comment>
      <xsl:value-of select="."/>
    </xsl:comment>
  </xsl:template>

<xsl:template match="text:alphabetical-index-mark-start">
<!--mettre des tests car il est possible qu'il n'y ait aucune clé-->
    <!--index indexName="{@text:key1}:{@text:key2}"-->
    <index>
    <xsl:attribute name="indexName">
   		<xsl:if test="not(@text:key1)">
   			<xsl:text>Index</xsl:text>
   		</xsl:if>
   		<xsl:if test="@text:key1"><xsl:value-of select="@text:key1"/></xsl:if>
   		<xsl:if test="@text:key2">:<xsl:value-of select="@text:key2"/></xsl:if>
   		<xsl:if test="@text:key3">:<xsl:value-of select="@text:key3"/></xsl:if>
   	</xsl:attribute>
    <term><xsl:value-of select="text:alphabetical-index-mark-start"/></term>
    </index>
  </xsl:template>

<xsl:template match="text:alphabetical-index-mark-end"/>

<xsl:template match="text:alphabetical-index-mark">
<xsl:variable name="index-mark"><xsl:value-of select="@text:key1"/></xsl:variable>    
<xsl:variable name="charDelimiter"><xsl:text>:</xsl:text></xsl:variable>  

<xsl:choose>
  <!-- marqueurs saisie DOCX : @text:string-value is empty -->
  <xsl:when test="@text:string-value=' '">
    <index>
      <xsl:attribute name="indexName">
        <xsl:choose>
          <xsl:when test="contains($index-mark,':')">
              <xsl:variable name="last">
                  <xsl:call-template name="substring-after-last">
                      <xsl:with-param name="string" select="$index-mark"/>
                      <xsl:with-param name="delimiter" select="$charDelimiter"/>
                  </xsl:call-template>
              </xsl:variable>
              <xsl:variable name="concatSep"><xsl:value-of select="concat(':',$last)"/></xsl:variable>
              <xsl:value-of select="substring-before($index-mark,$concatSep)"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>Index</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
        <term>
            <xsl:variable name="term">
                  <xsl:call-template name="substring-after-last">
                      <xsl:with-param name="string" select="$index-mark"/>
                      <xsl:with-param name="delimiter" select="$charDelimiter"/>
                  </xsl:call-template>
              </xsl:variable>
              <xsl:value-of select="$term"/>
        </term>
        <!--xsl:comment>docx</xsl:comment-->
      </index>
  </xsl:when>
  <!-- marqueurs saisie DOC : @text:string-value = term -->
  <xsl:otherwise>
    <index>
      <xsl:attribute name="indexName">
        <xsl:if test="not(@text:key1)"><xsl:text>Index</xsl:text></xsl:if><xsl:if test="@text:key1"><xsl:value-of select="@text:key1"/></xsl:if><xsl:if test="@text:key2">:<xsl:value-of select="@text:key2"/></xsl:if><xsl:if test="@text:key3">:<xsl:value-of select="@text:key3"/></xsl:if>
      </xsl:attribute>
      <!--xsl:comment>doc</xsl:comment-->
      <term>
        <xsl:value-of select="@text:string-value"/>
      </term>
    </index>
  </xsl:otherwise>
</xsl:choose>
</xsl:template>

<xsl:template name="substring-after-last">
  <xsl:param name="string" />
  <xsl:param name="delimiter" />
  <xsl:choose>
    <xsl:when test="contains($string, $delimiter)">
      <xsl:call-template name="substring-after-last">
        <xsl:with-param name="string" select="substring-after($string, $delimiter)" />
        <xsl:with-param name="delimiter" select="$delimiter" />
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$string" />
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="substring-before-last">
  <xsl:param name="string" />
  <xsl:param name="delimiter" />
  <xsl:choose>
    <xsl:when test="contains($string, $delimiter)">
      <xsl:call-template name="substring-before-last">
        <xsl:with-param name="string" select="substring-before($string, $delimiter)" />
        <xsl:with-param name="delimiter" select="$delimiter" />
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$string" />
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="text:alphabetical-index">
    <xsl:element name="index">
      <xsl:element name="title">
        <xsl:value-of select="text:index-body/text:index-title/text:p"/>
      </xsl:element>
      <xsl:apply-templates select="text:index-body"/>
    </xsl:element>
</xsl:template>

<xsl:template match="text:index-body">
    <xsl:for-each select="text:p[@text:style-name = 'Index 1']">
      <xsl:element name="indexentry">
        <xsl:element name="primaryie">
          <xsl:value-of select="."/>
        </xsl:element>
        <xsl:if test="key('secondary_children', generate-id())">
          <xsl:element name="secondaryie">
            <xsl:value-of select="key('secondary_children', generate-id())"/>
          </xsl:element>
        </xsl:if>
      </xsl:element>
    </xsl:for-each>
</xsl:template>

<!--xsl:template match="text:alphabetical-index-mark">
	<index>
          <xsl:attribute name="indexName"><xsl:if test="not(@text:key1)"><xsl:text>Index</xsl:text></xsl:if><xsl:if test="@text:key1"><xsl:value-of select="@text:key1"/></xsl:if><xsl:if test="@text:key2">:<xsl:value-of select="@text:key2"/></xsl:if><xsl:if test="@text:key3">:<xsl:value-of select="@text:key3"/></xsl:if></xsl:attribute>
		<term>
                  <xsl:value-of select="@text:string-value"/>
		</term>
	</index>
</xsl:template-->

<!-- Traitements des entrées d'index Open Office -->
<xsl:template match="text:user-index-mark-start">
	<index indexName="{@text:index-name}">
		<term>
			<xsl:value-of select="following-sibling::node()"/>
		</term>
	</index>
	<xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:user-index-mark-end"/>

<!-- ref croisées-->
<xsl:template match="text:bookmark-ref">
  <ref target="#{@text:ref-name}"><!-- type="crossref" -->
    <xsl:apply-templates/>
  </ref>
</xsl:template>

<xsl:template match="text:bookmark-start">
  <xsl:choose>
    <xsl:when test="contains(@text:name, 'GoBack')"></xsl:when>
    <xsl:otherwise>
      <anchor><!-- type="crossref" -->
        <xsl:attribute name="xml:id">
          <!--xsl:text>id_</xsl:text-->
          <xsl:value-of select="@text:name"/>
        </xsl:attribute>
      </anchor>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="text:bookmark-end"/>

<xsl:template match="text:bookmark">
  <xsl:choose>
    <xsl:when test="contains(@text:name, 'GoBack')"></xsl:when>
    <xsl:otherwise>
      <anchor>
        <xsl:attribute name="xml:id">
          <xsl:value-of select="@text:name"/>
        </xsl:attribute>
      </anchor>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

  <!--
These seem to have no obvious translation
-->

  <xsl:template match="text:endnotes-configuration"/>

  <xsl:template match="text:file-name"/>

  <xsl:template match="text:footnotes-configuration"/>

  <xsl:template match="text:linenumbering-configuration"/>

  <xsl:template match="text:list-level-style-bullet"/>

  <xsl:template match="text:list-level-style-number"/>

  <xsl:template match="text:list-style"/>

  <xsl:template match="text:outline-level-style"/>

  <xsl:template match="text:outline-style"/>

  <xsl:template match="text:s">
    <xsl:text> </xsl:text>
  </xsl:template>


  <xsl:template match="text:*"> [[[UNTRANSLATED <xsl:value-of
  select="name(.)"/>:     <xsl:apply-templates/>]]] </xsl:template>


  <!-- sections of the OO format we don't need at present -->

  <xsl:template match="office:automatic-styles"/>

  <xsl:template match="office:font-decls"/>

  <xsl:template match="office:meta"/>

  <xsl:template match="office:script"/>

  <xsl:template match="office:settings"/>

  <xsl:template match="office:styles"/>

  <xsl:template match="style:*"/>


  <xsl:template match="dc:*">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="meta:creation-date">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="meta:editing-cycles"/>

  <xsl:template match="meta:editing-duration"/>

  <xsl:template match="meta:generator"/>

  <xsl:template match="meta:user-defined"/>

<xsl:template match="text:section">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:sequence-decl">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:sequence-decls">
  <xsl:apply-templates/>
</xsl:template>


<xsl:template match="text:sequence">
  <xsl:apply-templates/>
</xsl:template>


<xsl:template match="text:section-source"/>


<xsl:template match="text:soft-page-break">
</xsl:template>

<xsl:template name="stars">
   <xsl:param name="n"/>
   <xsl:if test="$n &gt;0">
     <xsl:text>*</xsl:text>
     <xsl:call-template name="stars">
       <xsl:with-param name="n">
	 <xsl:value-of select="$n - 1"/>
       </xsl:with-param>
     </xsl:call-template>
   </xsl:if>
</xsl:template>

<xsl:template match="text:change|text:changed-region|text:change-end|text:change-start">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:table-of-content"/>
<xsl:template match="text:index-entry-chapter"/>
<xsl:template match="text:index-entry-page-number"/>
<xsl:template match="text:index-entry-tab-stop"/>
<xsl:template match="text:index-entry-text"/>
<xsl:template match="text:index-title-template"/>
<xsl:template match="text:table-of-content-entry-template"/>
<xsl:template match="text:table-of-content-source"/>

  <xsl:template match="office:text">
	<front>
    <titlePage>
      <docTitle>
        <xsl:if test="//text:p[@text:style-name='adsurtitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsurtitre']/@style:name]">
      		<xsl:call-template name="supTitle"/>
      	</xsl:if>
      	<!--xsl:if test="//text:h[@text:outline-level='1']"-->
      		<xsl:call-template name="mainTitle"/>
      <!--		<titlePart type="main" style="T_3_Article">
      			<xsl:apply-templates select="//text:h[@text:outline-level='1'][1]/text()|//text:h[@text:outline-level='1'][1]/text:span"/>
   			 </titlePart>-->
      	<!--/xsl:if-->
      	<xsl:if test="//text:p[@text:style-name='adSousTitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adSousTitre']/@style:name]">
      		<xsl:call-template name="subTitle"/>
      	</xsl:if>
      	<!--xsl:if test="//text:p[@text:style-name='adTitreTraduit']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTitreTraduit']/@style:name]"-->
      	<xsl:for-each select="//text:p[@text:style-name='adTitreTraduit']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTitreTraduit']/@style:name]">
      		<titlePart type="alt" style="T_0_Article_UK">
      			 <xsl:apply-templates/>
      		</titlePart>
      		</xsl:for-each>
      	<!--/xsl:if-->
<!-- titre et sous-titre langue inv -->
		<xsl:if test="text:p[@text:style-name='adtitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitre_5f_inv']/@style:name]">
  <xsl:variable name="readOrder">
    <xsl:choose>
      <xsl:when test="//office:automatic-styles/style:style[@style:name='adtitre_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
        <xsl:text>rtl</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ltr</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
	<titlePart style="T_inv" rend="{$readOrder}" type="alt" xml:lang="##">
		<xsl:value-of select="text:p[@text:style-name='adtitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitre_5f_inv']/@style:name]"/>
	</titlePart>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
	</xsl:if>
	<xsl:if test="text:p[@text:style-name='adsoustitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsoustitre_5f_inv']/@style:name]">
  <xsl:variable name="readOrder">
    <xsl:choose>
      <xsl:when test="//office:automatic-styles/style:style[@style:name='adsoustitre_5f_inv']/style:paragraph-properties/@style:writing-mode='rl-tb'">
        <xsl:text>rtl</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ltr</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
	<titlePart style="T_sousT_inv" rend="{$readOrder}" xml:lang="##" type="sub">
		<xsl:value-of select="text:p[@text:style-name='adsoustitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsoustitre_5f_inv']/@style:name]"/>
	</titlePart>
	<!--<xsl:text disable-output-escaping="yes">
	</xsl:text>-->
</xsl:if>

      </docTitle>
    <xsl:if test="//text:p[@text:style-name='adauteur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteur']/@style:name]">
<!--      <byline>-->
      <xsl:for-each select="//text:p[@text:style-name='adauteur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteur']/@style:name]">
        <docAuthor style="txt_auteur">
          <xsl:apply-templates/>
        </docAuthor>
        <!-- /!\ changement de la position du byline -->
        <xsl:if test="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name][1]">
            <byline>
        		<xsl:call-template name="affiliation_text"/>
            </byline>
        	<!--	<xsl:value-of select="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name][1]"/>-->
        </xsl:if>
        <xsl:if test="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]">
            <byline style="auteur_Courriel">
                <email>
				<ref>
                  <xsl:attribute name="target">mailto:<xsl:value-of select="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]"/></xsl:attribute>
                  <xsl:value-of select="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]"/>

				</ref>
        	</email>
            </byline>
        </xsl:if>
<!-- plusieurs paragraphes de rattachement après le nom de l'auteur mais sans adCAaffiliation (scénario 1)-->
        <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][not(child::text:span[@text:style-name='adCAaffiliation'])]">
            <xsl:variable name="testNext">
                <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
            </xsl:variable>
            <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][following-sibling::text:p=$testNext]">
                <xsl:variable name="affCount">
                    <xsl:value-of select="count(preceding::text:p[@text:style-name='adrattachement'])+1"/>
                </xsl:variable>
                <byline style="auteur_Institution">
                    <affiliation>
                      <xsl:attribute name="xml:id">
                        <xsl:choose>
                            <xsl:when test="$affCount &lt; 10">
                                <xsl:value-of select="concat('aff0',$affCount)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat('aff',$affCount)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                      </xsl:attribute> 
                      <xsl:apply-templates/>
                    </affiliation>
                </byline>
      </xsl:for-each>
            </xsl:if>
<!-- plusieurs paragraphes de rattachement après le nom de l'auteur : affiliations isolées via le style de caractères adCAaffiliation (scénario bspf) -->
    <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][child::text:span[@text:style-name='adCAaffiliation']][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][child::text:span[@text:style-name='adCAaffiliation']]">
            <xsl:variable name="testNext">
                <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
            </xsl:variable>
            <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]">
                <xsl:variable name="affCount">
                    <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                </xsl:variable>
                <byline style="auteur_Institution">
                      <xsl:apply-templates mode="front"/>
      </byline>
            </xsl:for-each>
    </xsl:if>  
      </xsl:for-each>
    </xsl:if>
<!-- contributeur -->
<xsl:if test="//text:p[@text:style-name='adcollaborateur']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateur']/@style:name]">
    <xsl:for-each select="//text:p[@text:style-name='adcollaborateur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateur']/@style:name]">
	<xsl:call-template name="contributeur"/>
        <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][not(child::text:span[@text:style-name='adCAaffiliation'])]">
            <xsl:variable name="testNext">
                <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
            </xsl:variable>
            <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][not(child::text:span[@text:style-name='adCAaffiliation'])][following-sibling::text:p=$testNext]">
                <xsl:variable name="affCount">
                    <xsl:value-of select="count(preceding::text:p[@text:style-name='adrattachement'])+1"/>
                </xsl:variable>
                <byline style="auteur_Institution">
                    <affiliation>
                      <xsl:attribute name="xml:id">
                        <xsl:choose>
                            <xsl:when test="$affCount &lt; 10">
                                <xsl:value-of select="concat('aff0',$affCount)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat('aff',$affCount)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                      </xsl:attribute> 
                      <xsl:apply-templates/>
                    </affiliation>
                </byline>
              </xsl:for-each>
            </xsl:if>
        <xsl:if test="following-sibling::text:p[@text:style-name='adrattachement'][child::text:span[@text:style-name='adCAaffiliation']][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement'][1]/@style:name][child::text:span[@text:style-name='adCAaffiliation']]">
            <xsl:variable name="testNext">
                <xsl:copy-of select="following-sibling::text:p[@text:style-name!='adrattachement'][1]"/>
            </xsl:variable>
            <xsl:for-each select="following-sibling::text:p[@text:style-name='adrattachement'][following-sibling::text:p=$testNext]">
                <xsl:variable name="affCount">
                    <xsl:value-of select="count(preceding::text:span[@text:style-name='adCAaffiliation'])+1"/>
                </xsl:variable>
                <byline style="auteur_Institution">
                      <xsl:apply-templates mode="front"/>
                </byline>
            </xsl:for-each>
        </xsl:if> 
    </xsl:for-each>
</xsl:if>
	<xsl:if test="text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]">
		<xsl:apply-templates select="text:p[@text:style-name='adauteurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteurs']/@style:name]" mode="titlePage"/>
        <xsl:for-each select="text:p[@text:style-name='adrattachement'][not(preceding::text:p[@text:style-name='adcollaborateurs'])]|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement']/@style:name][not(preceding::text:p[@text:style-name='adcollaborateurs'])]">
            <byline style="auteur_Institution">
                <xsl:apply-templates/>
            </byline>
        </xsl:for-each>
	</xsl:if>
	<xsl:if test="text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]">
		<xsl:apply-templates select="text:p[@text:style-name='adcollaborateurs']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateurs']/@style:name]" mode="titlePage"/>
        <xsl:for-each select="text:p[@text:style-name='adrattachement'][preceding::text:p[@text:style-name='adcollaborateurs']]|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement']/@style:name][preceding::text:p[@text:style-name='adcollaborateurs']]">
            <byline style="auteur_Institution">
               <xsl:apply-templates/>
            </byline>
        </xsl:for-each>
	</xsl:if>
    <xsl:if test="text:p[@text:style-name='adrattachement']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrattachement']/@style:name]">
	</xsl:if>
    </titlePage>
    <xsl:if test="text:p[contains(@text:style-name,'adresume')]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume']/@style:name]|text:p[contains(@text:style-name,'admotscles')]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name]">
  		<div type="resume_motscles">
			<xsl:apply-templates select="text:p[@text:style-name='adresume']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume']/@style:name]|text:p[@text:style-name='admotscles']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles']/@style:name]|text:p[@text:style-name='adresumeital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresumeital']/@style:name]|text:p[@text:style-name='admotsclesital']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotsclesital']/@style:name]|text:p[@text:style-name='adresume_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adresume_5f_inv']/@style:name]|text:p[@text:style-name='admotscles_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admotscles_5f_inv']/@style:name]" mode="front"/>
		</div>
  	</xsl:if>
    <xsl:if test="text:p[starts-with(@text:style-name,'note_3a_')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'note_3a_')]/@style:name]">
        <xsl:apply-templates select="text:p[starts-with(@text:style-name,'note_3a_')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'note_3a_')]/@style:name]" mode="front"/>
    </xsl:if>
    <xsl:if test="text:p[contains(@text:style-name,'adchapo')]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adchapo']/@style:name]">
        <argument>
            <xsl:apply-templates select="text:p[@text:style-name='adchapo']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adchapo']/@style:name]" mode="front"/>
        </argument>
    </xsl:if>
    <xsl:if test="text:p[starts-with(@text:style-name,'adarcheoA-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adarcheoA-')]/@style:name]">
    	<div type="archeo">
    		<xsl:apply-templates select="text:p[starts-with(@text:style-name,'adarcheoA-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adarcheoA-')]/@style:name]" mode="front"/>
    	</div>
    </xsl:if>
    <xsl:if test="text:p[starts-with(@text:style-name,'adorg-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adorg-')]/@style:name]">
    	<div type="partenaires">
    		<xsl:apply-templates select="text:p[starts-with(@text:style-name,'adorg-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adorg-')]/@style:name]" mode="front"/>
    	</div>
    </xsl:if>
    <xsl:if test="text:p[starts-with(@text:style-name,'adlien-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adlien-')]/@style:name]">
    	<div type="data">
    		<xsl:apply-templates select="text:p[starts-with(@text:style-name,'adlien-')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@text:style-name,'adlien-')]/@style:name]" mode="front"/>
    	</div>
    </xsl:if>
  	<xsl:if test="text:p[@text:style-name='adepigrapheF']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adepigrapheF']/@style:name]|text:p[@text:style-name='adremerciements']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adremerciements']/@style:name]|text:p[@text:style-name='addedicace']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addedicace']/@style:name]">
  		<div type="prelim">
  			<xsl:apply-templates select="text:p[@text:style-name='adepigrapheF']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adepigrapheF']/@style:name]|text:p[@text:style-name='adremerciements']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adremerciements']/@style:name]|text:p[@text:style-name='addedicace']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addedicace']/@style:name]" mode="front"/>
  		</div>
  	</xsl:if>

  </front>
    <body>
    <div type="chapitre" xml:id="mainDiv">
      <xsl:variable name="Body">
	<!--HEAD level="1" magic="true">Start</HEAD-->
        <xsl:apply-templates/>
      </xsl:variable>
      <!-- debug
      <xsl:result-document href="/tmp/temp.xml">
	<xsl:copy-of select="$Body"/>
      </xsl:result-document>
      -->
      <xsl:variable name="Body2">
	<xsl:for-each select="$Body">
	  <xsl:apply-templates mode="pass1"/>
	</xsl:for-each>
      </xsl:variable>
      <xsl:for-each select="$Body2">
        <xsl:for-each-group select="tei:*" group-starting-with="tei:HEAD[@level='2']">
          <xsl:choose>
            <xsl:when test="self::tei:HEAD[@level='2']">
	      <xsl:call-template name="group-by-section"/>
            </xsl:when>
            <xsl:otherwise>
	      <xsl:call-template name="inSection"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each-group>
      </xsl:for-each>
      </div>
    </body>
    <xsl:if test="text:p[@text:style-name='Titre-section-biblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-biblio']/@style:name]|text:p[@text:style-name='Titre-section-annexe']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-annexe']/@style:name]">
    <back>
	<xsl:if test="text:p[@text:style-name='Titre-section-biblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-biblio']/@style:name]">
		<xsl:call-template name="biblioBack"/>
	</xsl:if>
	<xsl:if test="text:p[@text:style-name='Titre-section-annexe']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-section-annexe']/@style:name]">
		<xsl:call-template name="annexeBack"/>
	</xsl:if>
  </back>
  </xsl:if>
  </xsl:template>

<xsl:template match="text:h[@text:outline-level='3'][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]"/>
<xsl:template match="text:h[@text:outline-level='4'][preceding-sibling::text:p[@text:style-name='Titre-section-biblio']]"/>

<xsl:template name="contributeur">
<!--	<xsl:for-each select="//text:p[@text:style-name='adcollaborateur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateur']/@style:name]">-->
		<byline style="txt_collaborateur">
			<xsl:apply-templates/>
        </byline>
        <xsl:if test="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name]">
            	<xsl:call-template name="contrib_institut"/>
            </xsl:if>
        <xsl:if test="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]">
        	<byline style="auteur_Courriel">
                <email>
				<ref>
                  <xsl:attribute name="target">mailto:<xsl:value-of select="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]"/></xsl:attribute>
                  <xsl:value-of select="following-sibling::text:p[@text:style-name='admail'][1]|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail'][1]/@style:name]"/>
				</ref>
        	</email>
            </byline>
        </xsl:if>
<!--	</xsl:for-each>-->
</xsl:template>

<xsl:template name="affiliation_text">
	<xsl:for-each select="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name][1]">
		<affiliation style="auteur_Institution">
			<xsl:apply-templates/>
		</affiliation>
	</xsl:for-each>
</xsl:template>

<xsl:template name="contrib_institut">
	<xsl:for-each select="following-sibling::text:p[@text:style-name='adinstitution'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution'][1]/@style:name]">
		<byline style="auteur_Institution">
			<xsl:apply-templates/>
		</byline>
	</xsl:for-each>
</xsl:template>


<xsl:template match="text:p[@text:style-name='adinstitution']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
    <byline style="auteur_Institution">
	   <xsl:apply-templates/>
    </byline>
</xsl:template>
    
<xsl:template name="mainTitle">
	<xsl:for-each select="//text:h[@text:outline-level='1']">
	<titlePart type="main" style="T_3_Article">
      	<xsl:apply-templates/>
    </titlePart>
    </xsl:for-each>
    <xsl:for-each select="//text:p[@text:style-name='Titre-recension']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-recension']/@style:name]">
		<titlePart type="main" style="T_3_Article">
     		<xsl:apply-templates/>
     	</titlePart>
     </xsl:for-each>
</xsl:template>

<xsl:template name="supTitle">
	<xsl:for-each select="//text:p[@text:style-name='adsurtitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsurtitre']/@style:name]">
		  <titlePart type="sup" style="T_Surtitre">
        	<xsl:apply-templates/>
      </titlePart>
    </xsl:for-each>
</xsl:template>

<xsl:template name="subTitle">
	<xsl:for-each select="//text:p[@text:style-name='adSousTitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adSousTitre']/@style:name]">
		<titlePart type="sub" style="T_SousTitre">
        	<xsl:apply-templates/>
        </titlePart>
    </xsl:for-each>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adepigrapheB']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adepigrapheB']/@style:name]">
	<epigraph>
		<quote style="txt_Epigraphe">
			<xsl:apply-templates/>
		</quote>
        <xsl:if test="following-sibling::text:p[1][@text:style-name='adsources']">
            <xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='adsources']" mode="inQuote"/>
        </xsl:if>
	</epigraph>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adauteursect']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteursect']/@style:name]">
    <xsl:choose>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]|preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Titre-recension']/@style:name]">
        </xsl:when>
   <xsl:otherwise>
    <docAuthor style="auteur_div"><xsl:apply-templates/></docAuthor>
       </xsl:otherwise>
         </xsl:choose>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adepigrapheF']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adepigrapheF']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adcollaborateur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcollaborateur']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adTitreTraduit']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adTitreTraduit']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adtitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitre_5f_inv']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adsoustitre_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsoustitre_5f_inv']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adauteur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteur']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adouvrage_5f_reference']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_reference']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adrecension_5f_titre_5f_biblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension_5f_titre_5f_biblio']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adrecension-biblio']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adinstitution']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='admail']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='admail']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adSousTitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adSousTitre']/@style:name]"/>
<xsl:template match="text:p[@text:style-name='adsurtitre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adsurtitre']/@style:name]"/>

<!--revues.org-->
<xsl:template match="text:p[@text:style-name='Titre_20_oeuvre']">
</xsl:template>
<xsl:template match="text:p[@text:style-name='Auteur_20_oeuvre']">
</xsl:template>
<xsl:template match="text:p[@text:style-name='Notice_20_Biblio_20_oeuvre']">
</xsl:template>
<xsl:template match="text:p[@text:style-name='Date_20_publi_20_oeuvre']">
</xsl:template>

<!-- adinclusion traitement des encadrés dans l'article -->
<xsl:template match="text:p[@text:style-name='adinclusion']|//text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinclusion']/@style:name]">
	<xsl:choose>
		<xsl:when test="preceding-sibling::text:p[@text:style-name='Titre-section-annexe']">
		</xsl:when>
		<xsl:otherwise>
			<floatingText type="encadre" subtype="##">
				<group>
					<xi:include>
						<xsl:attribute name="href"><xsl:value-of select="concat(.,'.xml')"/></xsl:attribute>
						<xsl:attribute name="xpointer"><xsl:text>text</xsl:text></xsl:attribute>
					</xi:include>
				</group>
			</floatingText>
		</xsl:otherwise>
	</xsl:choose>
	<!--xsl:apply-templates/-->
</xsl:template>

<!--Théâtre-->
<xsl:template match="text:p[@text:style-name='addidascalie']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='addidascalie']/@style:name]">
	<stage style="txt_didascalie">
		<xsl:apply-templates/>
	</stage>
</xsl:template>

<xsl:template match="text:span[@text:style-name='adCAdidascalie']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAdidascalie']/@style:name]">
	<stage style="typo_didasc">
		<xsl:apply-templates/>
	</stage>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adreplique']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adreplique']/@style:name]">
	<xsl:choose>
		<xsl:when test="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]">
			<sp>
				<xsl:attribute name="who"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></xsl:attribute>
				<xsl:call-template name="spreplique"/>
				<p style="txt_replique"><xsl:apply-templates/></p>
			</sp>
		</xsl:when>
		<xsl:otherwise>
			<p style="txt_replique"><xsl:apply-templates/></p>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="spreplique">
	<speaker style="typo_loc">
		<xsl:for-each select="descendant::text:span[@text:style-name='adCAlocuteur']">
			<xsl:apply-templates select="text()|node()"/>
		</xsl:for-each>
	</speaker>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adlignevers']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adlignevers']/@style:name]">
	<xsl:choose>
		<xsl:when test="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]">
			<sp>
				<speaker style="typo_loc"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></speaker>
				<l style="txt_ligne_vers"><xsl:apply-templates/></l>
			</sp>
		</xsl:when>
		<xsl:otherwise>
			<l style="txt_ligne_vers"><xsl:apply-templates/></l>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="//text:p[@text:style-name='adlignevers']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adlignevers']/@style:name]">
<sp><xsl:attribute name="who"><xsl:value-of select="concat(text:span[@text:style-name='adCAlocuteur'],'-')"/></xsl:attribute>
	<xsl:choose>
		<xsl:when test="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]">
				<speaker style="typo_loc"><xsl:value-of select="text:span[@text:style-name='adCAlocuteur']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAlocuteur']/@style:name]"/></speaker>
				<l style="txt_ligne_vers"><xsl:apply-templates/></l>
		</xsl:when>
		<xsl:otherwise>
			<l style="txt_ligne_vers"><xsl:apply-templates/></l>
		</xsl:otherwise>
	</xsl:choose>
	<!--xsl:if test="./following-sibling::text:p[@text:style-name='adlignevers']">
		grou<l style="txt_vers">
		<xsl:apply-templates select="./following-sibling::text:p[@text:style-name='adlignevers']" mode="insp"/>
		</l>
	</xsl:if-->
</sp>
</xsl:template>

<!--
<xsl:template match="text:p[@text:style-name='adlignevers']/text:line-break">
	<xsl:text disable-output-escaping="yes">&lt;/l&gt;</xsl:text>
	<xsl:text disable-output-escaping="yes">&lt;l style="txt_vers"&gt;</xsl:text>
	<xsl:apply-templates/>
</xsl:template>
-->

<xsl:template match="text:p[@text:style-name='adreplique']/text:line-break">
<!--xsl:text disable-output-escaping="yes">&lt;/p&gt;</xsl:text><xsl:text disable-output-escaping="yes">&lt;p style="txt_replique"&gt;</xsl:text-->
<lb/>
		<xsl:apply-templates/>
</xsl:template>

<!-- poésie -->
<xsl:template match="text:p[@text:style-name='advers']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='advers']/@style:name]">
	<l style="txt_vers">
		<xsl:if test="descendant::text:span[@text:style-name='adCAnumvers']|descendant::text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnumvers']/@style:name]">
			<xsl:attribute name="n">
				<xsl:value-of select="descendant::text:span[@text:style-name='adCAnumvers']|descendant::text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnumvers']/@style:name]|text:span[@text:style-name='adCAnumvers']|text:span[@text:style-name=//style:style[@style:parent-style-name='adCAnumvers']/@style:name]"/>
			</xsl:attribute>
		</xsl:if>
		<xsl:apply-templates/>
	</l>
</xsl:template>

<xsl:template match="text:p[@text:style-name='advers']/text:tab">
	<caesura/>
		<xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:p[@text:style-name='advers_5f_inv']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='advers_5f_inv']/@style:name]">
	<l rend="rtl" style="txt_vers_inv">
		<xsl:if test="text:span[@text:style-name='adCAnumvers']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnumvers']/@style:name]">
			<xsl:attribute name="n">
				<xsl:value-of select="text:span[@text:style-name='adCAnumvers']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnumvers']/@style:name]"/>
			</xsl:attribute>
		</xsl:if>
		<xsl:apply-templates/>
	</l>
</xsl:template>

<xsl:template match="text:p[@text:style-name='advers_5f_inv']/text:tab">
	<caesura/>
		<xsl:apply-templates/>
</xsl:template>

<xsl:template match="text:span[@text:style-name='adCAnumvers']|text:span[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAnumvers']/@style:name]"/>
	<!--num style="typo_numvers"><xsl:apply-templates/></num>
</xsl:template-->

<!--Insertion media-->
<xsl:template match="text:p[@text:style-name='addescmedia']/draw:frame">
<xsl:variable name="nameFilemedia"><xsl:value-of select="substring-after(draw:plugin/@xlink:href,'/br/')"/></xsl:variable>
        <media>
          <xsl:attribute name="url">
            <xsl:value-of select="draw:plugin/@xlink:href"/>
          </xsl:attribute>
          <xsl:attribute name="mimeType">
            <xsl:text>??</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="xml:id">
            <xsl:value-of select="substring-before($nameFilemedia,'.')"/>
          </xsl:attribute>
          <xsl:attribute name="width">
            <xsl:value-of select="@svg:width"/>
          </xsl:attribute>
          	<desc>
          		<xsl:value-of select="../text()"/>
          	</desc>
        </media>
</xsl:template>
<xsl:template match="text:p[@text:style-name='addescmedia']/text()"/>

  <xsl:template name="group-by-section">
    <xsl:variable name="ThisHeader" select="number(@level)"/>
    <xsl:variable name="NextHeader" select="number(@level)+1"/>
    <xsl:choose>
      <xsl:when test="@magic">
	  <xsl:for-each-group select="current-group() except ."
			      group-starting-with="tei:HEAD[number(@level)=$NextHeader]">
	    <xsl:choose>
	      <xsl:when test="self::tei:HEAD">
		<xsl:call-template name="group-by-section"/>
	      </xsl:when>
	    <xsl:otherwise>
	      <xsl:call-template name="inSection"/>
	    </xsl:otherwise>
	    </xsl:choose>
	  </xsl:for-each-group>
      </xsl:when>
      <xsl:otherwise>
	<div>
	<xsl:attribute name="type">section<xsl:value-of select="$ThisHeader -1"/></xsl:attribute>
	  <!-- commenté : pas d'@rend sur les div
	  <xsl:choose>
	    <xsl:when test="starts-with(@style,'Heading')"/>
	    <xsl:when test="@style">
	      <xsl:attribute name="rend" select="@style"/>
	    </xsl:when>
	  </xsl:choose>-->
	  <!-- div typée, on récupère le préfixe du nom de style -->
	  <xsl:choose>
	  	<xsl:when test="contains(@style,'-')">
	  		<xsl:attribute name="subtype" select="substring-after(@style,'-')"/>
	  	</xsl:when>
	  </xsl:choose>
	  <xsl:if test="not(@interpolated='true')">
	<!-- traitement des bibl des recensions -->
	  <!--xsl:choose>
	  	<xsl:when test="contains(@style,'recension')">
	  		<bibl>
				<xsl:variable name="plop"><xsl:value-of select="."/></xsl:variable>
				plop=<xsl:value-of select="$plop"/>|
	  			<xsl:for-each select="preceding::text:p[@text:style-name='adouvrage_5f_auteur'][following-sibling::text:h=$plop]">
	  				**
				</xsl:for-each>
	  			<title><xsl:apply-templates mode="pass1"/></title>
	  		</bibl>
	  	</xsl:when>
	  	<xsl:otherwise-->
	  	  <head>
			  <xsl:attribute name="subtype">level<xsl:value-of select="$ThisHeader -1"/></xsl:attribute>
			  <xsl:attribute name="style">T_<xsl:value-of select="$ThisHeader -1"/></xsl:attribute>
	  	    <xsl:apply-templates mode="pass1"/>
	  	  </head>
	    <!--/xsl:otherwise>
	  </xsl:choose-->
	  </xsl:if>
	  <xsl:for-each-group select="current-group() except ."
			      group-starting-with="tei:HEAD[number(@level)=$NextHeader]">
	    <xsl:choose>
	      <xsl:when test="self::tei:HEAD">
		<xsl:call-template name="group-by-section"/>
	      </xsl:when>
	    <xsl:otherwise>
		<xsl:call-template name="inSection"/>
	    </xsl:otherwise>
	    </xsl:choose>
	  </xsl:for-each-group>
	</div>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="inSection">
    <xsl:for-each-group select="current-group()"
			group-adjacent="if (self::tei:GLOSS)
					then 1
					else 2">
      <xsl:choose>
	<xsl:when test="current-grouping-key()=1">
	  <list type="gloss">
	    <xsl:for-each select="current-group()">
	      <xsl:element name="{@n}">
		<xsl:apply-templates mode="pass2"/>
	      </xsl:element>
	    </xsl:for-each>
	  </list>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:for-each select="current-group()">
	    <xsl:apply-templates select="." mode="pass2"/>
	  </xsl:for-each>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:template>

  <xsl:template match="@*|text()|comment()|processing-instruction()" mode="pass1">
    <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="tei:p[not(node())]" mode="pass1">
  </xsl:template>

  <xsl:template match="tei:HEAD" mode="pass1">
    <xsl:if test="preceding-sibling::tei:HEAD">
      <xsl:variable name="prev"
		    select="xs:integer(number(preceding-sibling::tei:HEAD[1]/@level))"/>
      <xsl:variable name="current"
		    select="xs:integer(number(@level))"/>
	<xsl:if test="($current - $prev) &gt;1 ">
	  <!--<xsl:message>Walk from <xsl:value-of select="$prev"/> to <xsl:value-of select="$current"/></xsl:message>-->
	  <xsl:for-each
	      select="$prev + 1   to $current - 1 ">
	    <HEAD interpolated='true' level="{.}"/>
	  </xsl:for-each>
	</xsl:if>
    </xsl:if>
    <xsl:copy>
    <xsl:apply-templates
	select="*|@*|processing-instruction()|comment()|text()"
	mode="pass1"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="*" mode="pass1">
    <xsl:copy>
      <xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass1"/>
    </xsl:copy>
  </xsl:template>


  <!-- second pass -->
  <xsl:template match="tei:p[not(*) and normalize-space(.)='']"
		mode="pass2">
  </xsl:template>

  <xsl:template match="@*|comment()|processing-instruction()" mode="pass2">
    <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="*" mode="pass2">
    <xsl:copy>
      <xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass2"/>
    </xsl:copy>
  </xsl:template>


  <xsl:template match="text()" mode="pass2">
    <xsl:value-of select="."/>
  </xsl:template>


  <xsl:template match="tei:title" mode="pass2">
    <xsl:choose>
      <xsl:when test="parent::tei:div|parent::tei:body">
	<head>
	  <xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass2"/>
	</head>
      </xsl:when>
      <xsl:otherwise>
	<xsl:copy>
	  <xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass2"/>
	</xsl:copy>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- third pass -->

    <xsl:template match="@*|comment()|processing-instruction()" mode="pass3">
        <xsl:copy-of select="."/>
    </xsl:template>

    <xsl:template match="*" mode="pass3">
        <xsl:copy>
            <xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass3"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match="text()" mode="pass3">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="tei:div[not(@type)]" mode="pass3">
      <div type="div{count(ancestor-or-self::tei:div)}">
	<xsl:apply-templates select="*|@*|processing-instruction()|comment()|text()" mode="pass3"/>
      </div>
    </xsl:template>

    <xsl:function name="tei:inlineStyles"  as="xs:string">
      <xsl:param name="name"/>
      <xsl:param name="context"/>
      <xsl:choose>
	<xsl:when test="starts-with($name,'tei_5f_')">
	  <xsl:value-of select="substring($name,8)"/>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:variable name="r">
	    <xsl:for-each select="$context/key('STYLES',$name)">
	      <xsl:if
		  test="style:paragraph-properties/@fo:text-align">
		<xsl:value-of
		    select="style:paragraph-properties/@fo:text-align"/>
		<xsl:text> </xsl:text>
	  </xsl:if>
	  <xsl:if
	      test="style:text-properties[starts-with(@style:text-position,'super')]">
	    <xsl:text>sup </xsl:text>
	  </xsl:if>

	  <xsl:if test="style:text-properties/@fo:color and not(style:text-properties/@fo:color='transparent')">
	    <xsl:text> color(</xsl:text>
	    <xsl:value-of select="style:text-properties/@fo:color"/>
	    <xsl:text>)</xsl:text>
	  </xsl:if>

	  <xsl:if test="style:text-properties/@fo:background-color and not(style:text-properties/@fo:background-color='transparent')">
	    <xsl:text> background-color(</xsl:text>
	    <xsl:value-of select="style:text-properties/@fo:background-color"/>
	    <xsl:text>)</xsl:text>
	  </xsl:if>

	  <xsl:if
	      test="style:text-properties[starts-with(@style:text-position,'sub')]">
	    <xsl:text>sub </xsl:text>
	  </xsl:if>

	  <xsl:if test="style:text-properties[@fo:font-weight='bold']">
	    <xsl:text>bold </xsl:text>
	 </xsl:if>

	 <xsl:if
	     test="style:text-properties[@style:text-underline-type='double']">
	   <xsl:text>underdoubleline </xsl:text>
	 </xsl:if>

	 <xsl:if
	     test="style:text-properties[@style:text-underline-style='solid']">
	   <xsl:text>underline </xsl:text>
	 </xsl:if>

	 <xsl:if
	     test="style:text-properties[@style:text-line-through-style='solid']">
	   <xsl:text>strikethrough </xsl:text>
	 </xsl:if>

	 <xsl:if
	     test="style:text-properties[@fo:font-variant='small-caps']">
	   <xsl:text>smallcaps </xsl:text>
	 </xsl:if>

	 <xsl:if test="style:text-properties[@fo:font-style='italic']">
	   <xsl:text>italic </xsl:text>
	 </xsl:if>

	    </xsl:for-each>
	  </xsl:variable>
	  <xsl:value-of select="normalize-space($r)"/>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:function>

<!-- ILLUSTRATIONS ET TABLEAUX -->
  <xsl:template match="draw:image">
    <xsl:choose>
      <xsl:when test="ancestor::draw:text-box">
		      <xsl:call-template name="findGraphic"/>
      </xsl:when>
      <!-- code hexa des équations… voir si conversion à la volée possible -->
      <xsl:when test="preceding-sibling::draw:object[child::*:math]"/>
      <xsl:when test="ancestor::draw:frame">
		      <xsl:call-template name="findGraphic"/>
      </xsl:when>
      <xsl:when test="parent::text:p[@text:style-name='Mediaobject']">
        <figure>
          <xsl:call-template name="findGraphic"/>
          <head>
            <xsl:value-of select="."/>
          </head>
        </figure>
      </xsl:when>
      <xsl:otherwise>
        <figure>
          <xsl:call-template name="findGraphic"/>
        </figure>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="findGraphic">
    <xsl:choose>
      <!--xsl:when test="office:binary-data">
	<xsl:apply-templates/>
      </xsl:when-->
      <xsl:when test="not(@xlink:href)">
        <!--pas d'href, docx born-->
        <graphic>
          <xsl:attribute name="url">
            <xsl:value-of select="concat('../icono/br/',parent::draw:frame/@draw:name)"/>
          </xsl:attribute>
        </graphic>
      </xsl:when>
      <xsl:when test="@xlink:href">
        <!--@xlink:href = docx passé en doc-->
        <graphic>
          <xsl:attribute name="url">
           	<!--xsl:value-of select="@xlink:href"/-->
            <xsl:value-of select="concat('../icono',substring-after(@xlink:href,'icono'))"/>
          </xsl:attribute>
        </graphic>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

<xsl:template match="office:binary-data"/>

  <!-- drawing -->
  <xsl:template match="draw:plugin">
    <ptr target="{@xlink:href}"/>
  </xsl:template>

  <xsl:template match="draw:text-box">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="draw:frame">
    <xsl:choose>
      <xsl:when test="ancestor::draw:frame">
	<xsl:apply-templates/>
      </xsl:when>
      <xsl:otherwise>
	<!--figure-->
	  <xsl:apply-templates/>
	<!--/figure-->
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

<xsl:template match="text:p[@text:style-name='adtitretableau']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitretableau']/@style:name]">
</xsl:template>

<!-- interception des styles d'encadrés -->
<xsl:template match="text:p[starts-with(@text:style-name,'adenc')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adenc')]/@style:name]">
</xsl:template>

  <!-- tables -->
<xsl:template match="table:table">
    <xsl:choose>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_titre']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='Titre-recension']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
    </xsl:when>
    <xsl:when test="preceding::text:p[@text:style-name='adouvrage_5f_refbibliofull']|preceding::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
    </xsl:when>
         <xsl:otherwise>

<!-- Nombre de colonnes -->
<xsl:variable name="tableColumn">
  <xsl:choose>
    <xsl:when test="child::table:table-column/@table:number-columns-repeated and child::table:table-column[not(@table:number-columns-repeated)]">
      <xsl:value-of select="sum(child::table:table-column/@table:number-columns-repeated) + count(child::table:table-column[not(@table:number-columns-repeated)])"/>
    </xsl:when>
    <xsl:when test="child::table:table-column[not(@table:number-columns-repeated)]">
      <xsl:value-of select="count(child::table:table-column)"/>
    </xsl:when>
    <xsl:when test="child::table:table-column/@table:number-columns-repeated">
      <xsl:value-of select="sum(child::table:table-column/@table:number-columns-repeated)"/>
    </xsl:when>
    <xsl:otherwise/>
  </xsl:choose>
</xsl:variable>

    <xsl:variable name="cells" select="count(descendant::table:table-cell)"/>
    <xsl:variable name="rows">
    	<xsl:value-of select="count(descendant::table:table-row) "/>
    </xsl:variable>

    <!-- traitement différencié des encadrés et des tableaux -->
    <xsl:choose>
    	<xsl:when test="preceding-sibling::text:p[1][starts-with(@text:style-name,'adcartouche')]|preceding-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adcartouche')]/@style:name]">
    	</xsl:when>
      <xsl:when test="preceding-sibling::text:p[1][starts-with(@text:style-name,'adenc')]|preceding-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adenc')]/@style:name]">

        <xsl:variable name="precedingStyle">
          <xsl:value-of select="preceding-sibling::text:p[1]/@text:style-name"/>
        </xsl:variable>
        <xsl:variable name="styleEnc">
          <xsl:choose>
            <xsl:when test="starts-with($precedingStyle,'adenc')">
              <xsl:value-of select="preceding-sibling::text:p[1]/@text:style-name"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="//office:automatic-styles/style:style[@style:name=$precedingStyle]/@style:parent-style-name"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:variable>
        <xsl:variable name="titreEnc">
          <xsl:text>titreEnc</xsl:text><xsl:value-of select="substring-after($styleEnc,'adenc')"/>
        </xsl:variable>
        <xsl:variable name="nbEnc">
          <xsl:value-of select="count(preceding::text:p[starts-with(@text:style-name,'adenc')]) + count(preceding::text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'adenc')]/@style:name])"/>
        </xsl:variable>

        <floatingText type="encadre" n="{$nbEnc}">
        	<xsl:attribute name="subtype">
        		<xsl:value-of select="substring-after($styleEnc,'adenc')"/>
        	</xsl:attribute>
          <body>
            <div type="encadre">
             <xsl:if test="preceding-sibling::text:p[1] != ''">
              <head style="{$titreEnc}"><xsl:apply-templates select="preceding-sibling::text:p[1]/node()"/></head>
              </xsl:if>
            <!--            <xsl:apply-templates select="descendant::table:table-cell/*"/> -->
            <xsl:variable name="Body">
              <xsl:apply-templates select="descendant::table:table-cell/*" />
            </xsl:variable>

            <xsl:variable name="Body2">
              <xsl:for-each select="$Body">
                <xsl:apply-templates mode="pass1"/>
              </xsl:for-each>
            </xsl:variable>
            <xsl:for-each select="$Body2">
              <xsl:for-each-group select="tei:*" group-starting-with="tei:HEAD[@level='2']">
                <xsl:choose>
                  <xsl:when test="self::tei:HEAD[@level='2']">
                    <xsl:call-template name="group-by-section"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:call-template name="inSection"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:for-each-group>
            </xsl:for-each>
          </div>
          </body>
        </floatingText>

      </xsl:when>
      <xsl:otherwise>
 	<table rend="frame" cols="{$tableColumn}" rows="{$rows}">
   		<xsl:if test="@table:name">
     		<xsl:attribute name="xml:id">
       			<xsl:value-of select="@table:name"/>
     		</xsl:attribute>
   		</xsl:if>
		<xsl:if test="following-sibling::text:p[1][@text:style-name='adtitretableau']">
   			<xsl:call-template name="titretab1"/>
  		</xsl:if>
	    <xsl:if test="following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitretableau']/@style:name]">
             <xsl:call-template name="titretab1"/>
  <!--       <head>
                <xsl:value-of select="text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitretableau']/@style:name]"/>
	          </head>-->
	    </xsl:if>
 		<xsl:call-template name="generictable"/>
 	</table>
      </xsl:otherwise>
    </xsl:choose>
             </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="titretab1">
	<xsl:for-each select="following-sibling::text:p[1][@text:style-name='adtitretableau']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtitretableau']/@style:name]">
	<head>
   		<xsl:apply-templates/>
   	</head>
	</xsl:for-each>
</xsl:template>

<xsl:template name="generictable">
    <xsl:variable name="cells" select="count(descendant::table:table-cell)"/>
    <xsl:variable name="rows">
      <xsl:value-of select="count(descendant::table:table-row) "/>
    </xsl:variable>
    <xsl:variable name="cols">
      <xsl:value-of select="$cells div $rows"/>
    </xsl:variable>
    <!--xsl:variable name="numcols">
    	<xsl:choose>
        	<xsl:when test="child::table:table-column/@table:number-columns-repeated">
          		<xsl:value-of select="number(table:table-column/@table:number-columns-repeated+1)"/>
        	</xsl:when>
        	<xsl:otherwise>
          		<xsl:value-of select="$cols"/>
        	</xsl:otherwise>
      	</xsl:choose>
    </xsl:variable-->
    <xsl:apply-templates/>
</xsl:template>

<xsl:template name="colspec">
	<xsl:param name="left"/>
    	<xsl:if test="number($left &lt; ( table:table-column/@table:number-columns-repeated +2)  )">
      		<xsl:element name="colspec">
        		<xsl:attribute name="colnum">
          			<xsl:value-of select="$left"/>
        		</xsl:attribute>
        		<xsl:attribute name="colname">c
                    <xsl:value-of select="$left"/>
                </xsl:attribute>
      		</xsl:element>
      		<xsl:call-template name="colspec">
        		<xsl:with-param name="left" select="$left+1"/>
      		</xsl:call-template>
    	</xsl:if>
</xsl:template>

<xsl:template match="table:table-column">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="table:table-header-rows">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="table:table-header-rows/table:table-row">
    <row role="label">
      <xsl:apply-templates/>
    </row>
  </xsl:template>

<xsl:template match="table:table/table:table-row">
    <row>
      <xsl:apply-templates/>
    </row>
</xsl:template>

<!--<xsl:template match="table:table-cell/text:h">
  <xsl:apply-templates/>
</xsl:template> -->


<!-- Modification lourde pour l'ensemble des tableaux : on garde maintenant les paragraphes dans une cellule en désactivant le template suivant !!!!!!À tester!!!!!! Il faut donc utiliser adcellule quand on ne veut pas de structures dans les cellules -->
<!-- <xsl:template match="table:table-cell/text:p">
  <xsl:call-template name="applyStyle"/>
</xsl:template> -->

<xsl:template match="table:table-cell">
  <cell>
<xsl:variable name="currentStyle">
	<xsl:value-of select="descendant::text:p/@text:style-name"/>
</xsl:variable>
  	<xsl:attribute name="rendition">
  		<xsl:choose>
  			<xsl:when test="contains(@table:style-name,'Tableau')">
  				<xsl:value-of select="concat('#Cell',substring-after(@table:style-name,'Tableau'))"/>
  			</xsl:when>
  			<xsl:when test="contains(@table:style-name,'Tabla')">
  				<xsl:value-of select="concat('#Cell',substring-after(@table:style-name,'Tabla'))"/>
  			</xsl:when>
  			<xsl:when test="contains(@table:style-name,'Table')">
  				<xsl:value-of select="concat('#Cell',substring-after(@table:style-name,'Table'))"/>
  			</xsl:when>
        <xsl:when test="contains(@table:style-name,'Tabella')">
  				<xsl:value-of select="concat('#Cell',substring-after(@table:style-name,'Tabella'))"/>
  			</xsl:when>
        <xsl:when test="contains(@table:style-name,'Tabela')">
    				<xsl:value-of select="concat('#Cell',substring-after(@table:style-name,'Tabela'))"/>
  			</xsl:when>
  			<xsl:otherwise>
  			</xsl:otherwise>
  		</xsl:choose>
  	</xsl:attribute>
  	<xsl:if test="$OOstyles//style:style[@style:name=$currentStyle]/style:paragraph-properties/@fo:text-align">
		<xsl:attribute name="rend">
			<xsl:text>text-align:</xsl:text><xsl:value-of select="$OOstyles//style:style[@style:name=$currentStyle]/style:paragraph-properties/@fo:text-align"/><xsl:text>;</xsl:text>
		</xsl:attribute>
	</xsl:if>
    <xsl:if test="@table:number-columns-spanned &gt;'1'">
      <xsl:attribute name="cols">
        <xsl:value-of select="@table:number-columns-spanned"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="@table:number-rows-spanned &gt;'1'">
      <xsl:attribute name="rows">
        <xsl:value-of select="@table:number-rows-spanned"/>
      </xsl:attribute>
    </xsl:if>
    <!--xsl:if test="text:p[@text:style-name='adtetierecell']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adtetierecell']/@style:name]">
      <xsl:attribute name="role">label</xsl:attribute>
    </xsl:if-->
    <xsl:if test="text:h">
      <xsl:attribute name="role">label</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
  </cell>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adauteursignature']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteursignature']/@style:name]">
	<docAuthor style="txt_signature">
		<xsl:apply-templates/>
	</docAuthor>
</xsl:template>

</xsl:stylesheet>
