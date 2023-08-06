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



<!-- recension -->

<!-- block -->
<xsl:template match="text:p[@text:style-name='adouvrage_5f_titre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">

     <xsl:variable name="recension" select="."/>
     <xsl:variable name="recensionSuivante">
    	<xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name][1]"/>
    </xsl:variable>
    <xsl:variable name="recensionLast">
    	<xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_titre'][position()=last()]"/>
    </xsl:variable>

	<div type="recension">
	<!--recension = <xsl:value-of select="$recension"/>
	recensionSuivante = <xsl:value-of select="$recensionSuivante"/>
	recensionLast = <xsl:value-of select="$recensionLast"/>-->
		<!-- auteur et titre, date, référence -->
		<bibl>
		<xsl:for-each select="preceding-sibling::text:p[@text:style-name='adouvrage_5f_auteur'][following-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]=$recension]|preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_auteur']/@style:name][following-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]=$recension]">
       	  <author style="recension_auteur">
      	      <xsl:apply-templates/>
      	  </author>
      	</xsl:for-each>
      	<title style="recension_titre">
      	  <xsl:apply-templates/>
      	</title>
      	<xsl:if test="following-sibling::text:p[1][@text:style-name='adouvrage_5f_compltitre']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_compltitre']]">
      		<xsl:for-each select="following-sibling::text:p[1][@text:style-name='adouvrage_5f_compltitre']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_compltitre']]">
	      		<title style="recension_compl_titre" type="compl">
	      			<xsl:apply-templates/>
    	   		</title>
      		</xsl:for-each>
      		<!--xsl:choose>
          <xsl:when test="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][2]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']">
            <date>
              <xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][2]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']"/>
            </date>
          </xsl:when>
        <xsl:otherwise/>
      </xsl:choose>-->
      <xsl:for-each select="following-sibling::text:p[2][@text:style-name='adouvrage_5f_reference']|following-sibling::text:p[2][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_reference']]">
	      <xsl:apply-templates/>
      </xsl:for-each>
      	</xsl:if>
      	<xsl:choose>
          <xsl:when test="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_reference']/@style:name][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']">
            <date>
              <xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_reference']/@style:name][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']"/>
            </date>
          </xsl:when>
        <xsl:otherwise/>
      </xsl:choose>
      <xsl:for-each select="following-sibling::text:p[1][@text:style-name='adouvrage_5f_reference']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_reference']]">
	      <xsl:apply-templates/>
      </xsl:for-each>
      	</bibl>
      <!-- corps de la recension (avec test pour le traitement de la dernière recension qui n'a pas de recensionSuivante -->
	<xsl:choose>
	<xsl:when test="$recensionLast=''">
		<xsl:for-each select="following-sibling::text:*[preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']]">
			<xsl:choose>
        <xsl:when test="@text:style-name='adtitrefigure'">
          <figure style="titre_figure">
            <xsl:apply-templates select="descendant::draw:frame"/>
            <head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a"/>
		</head>
<!--              après le titre [1] : légende -->
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
          </figure>
        </xsl:when>
                <xsl:when test="local-name()='list'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
                  <xsl:when test="local-name()='table'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
        <xsl:when test="@text:style-name='Standard'">
					<p style="txt_Normal">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
        		<xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name">
          			<p style="txt_Normal">
    					<xsl:apply-templates/>
    				</p>
        		</xsl:when>
                 <xsl:when test="@text:style-name='adcontinued-para'">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
                </xsl:when>
                <xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
        		</xsl:when>
				<xsl:when test="@text:style-name='adcitationrom'">
					<quote style="txt_Citation" rend="quotation">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>
				<xsl:when test="@text:style-name='adrecension_5f_titre_5f_biblio' or @text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension_5f_titre_5f_biblio']/@style:name">
					<div type="bibliographie">
						<head style="titre_biblio"><xsl:apply-templates/></head>
            <listBibl>
						<xsl:for-each select="following-sibling::text:p[@text:style-name='adrecension-biblio'][following-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recensionSuivante]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recensionSuivante]">
							<bibl style="txt_Bibliographie"><xsl:apply-templates/></bibl>
						</xsl:for-each>
            </listBibl>
					</div>
				</xsl:when>
				<xsl:when test="@text:style-name='adauteursect'">
					<docAuthor style="auteur_recension">
      					<name><xsl:apply-templates/></name>
      					<xsl:if test="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
          					<xsl:for-each select="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
            					<affiliation style="auteur-recension-institution"><xsl:apply-templates/></affiliation>
         					 </xsl:for-each>
        				</xsl:if>
					</docAuthor>
				</xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:for-each>
		<!--xsl:for-each select="following-sibling::text:*[preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']]|following-sibling::text:*[preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]]">
			<xsl:choose>
				<xsl:when test="@text:style-name='Standard'">
					<p style="txt_Normal">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
				<xsl:when test="@text:style-name='adcitationrom'">
					<quote style="txt_Citation">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>
				<xsl:when test="@text:style-name='adauteursect'">
					<docAuthor style="auteur_recension">
      					<name><xsl:apply-templates/></name>
      					<xsl:if test="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
          					<xsl:for-each select="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
            					<affiliation style="auteur-recension-institution"><xsl:apply-templates/></affiliation>
         					 </xsl:for-each>
        				</xsl:if>
					</docAuthor>
				</xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:for-each-->
		</xsl:when>
		<xsl:otherwise>
			<xsl:for-each select="following-sibling::text:*[preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recension][following-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recensionSuivante]|following-sibling::text:*[preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recension][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recensionSuivante]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recension][following-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recensionSuivante]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recension][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recensionSuivante]">
			<xsl:choose>
        <xsl:when test="@text:style-name='adtitrefigure'">
					<figure style="titre_figure">
						<xsl:apply-templates select="descendant::draw:frame"/>
            <head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a"/>
		</head>
<!--              après le titre [1] : légende -->
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
          </figure>
				</xsl:when>
                 <xsl:when test="local-name()='list'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
                  <xsl:when test="local-name()='table'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
        <xsl:when test="@text:style-name='Standard'">
					<p style="txt_Normal">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
        		<xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name">
          			<p style="txt_Normal">
    					<xsl:apply-templates/>
    				</p>
        		</xsl:when>
                 <xsl:when test="@text:style-name='adcontinued-para'">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
                </xsl:when>
                <xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
        		</xsl:when>
				<xsl:when test="@text:style-name='adcitationrom'">
					<quote style="txt_Citation" rend="quotation">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>
				<xsl:when test="@text:style-name='adrecension_5f_titre_5f_biblio' or @text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension_5f_titre_5f_biblio']/@style:name">
					<div type="bibliographie">
						<head style="titre_biblio"><xsl:apply-templates/></head>
            <listBibl>
						<xsl:for-each select="following-sibling::text:p[@text:style-name='adrecension-biblio'][following-sibling::text:p[@text:style-name='adouvrage_5f_titre']=$recensionSuivante]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]=$recensionSuivante]">
							<bibl style="txt_Bibliographie"><xsl:apply-templates/></bibl>
						</xsl:for-each>
            </listBibl>
					</div>
				</xsl:when>
				<xsl:when test="@text:style-name='adauteursect'">
					<docAuthor style="auteur_recension">
      					<name><xsl:apply-templates/></name>
      					<xsl:if test="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
          					<xsl:for-each select="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
            					<affiliation style="auteur-recension-institution"><xsl:apply-templates/></affiliation>
         					 </xsl:for-each>
        				</xsl:if>
					</docAuthor>
				</xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:for-each>
		</xsl:otherwise>
	</xsl:choose>
	</div>
</xsl:template>

<!-- inline -->
<xsl:template match="text:p[@text:style-name='adouvrage_5f_refbibliofull']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">

  <xsl:variable name="recensionFull" select="."/>
    <xsl:variable name="recensionFullSuivante">
    	<xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull'][1]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name][1]"/>
    </xsl:variable>
    <xsl:variable name="recensionFullLast">
    	<xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull'][position()=last()]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name][position()=last()]"/>
    </xsl:variable>

  <div type="recension">
  <bibl style="recension_refbiblio">
    <xsl:apply-templates/>
    <xsl:if test="descendant::text:span[@text:style-name='adCAouvrage_5f_date']|descendant::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAouvrage_5f_date']/@style:name]">
		<date><xsl:value-of select="descendant::text:span[@text:style-name='adCAouvrage_5f_date']|descendant::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adCAouvrage_5f_date']/@style:name]"/></date>
    </xsl:if>
  </bibl>
  <xsl:choose>
  <!-- traitement de la dernière recension -->
  	<xsl:when test="$recensionFullLast=''">
  		<xsl:for-each select="following-sibling::text:*[preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']]">
			<xsl:choose>
        <xsl:when test="@text:style-name='adtitrefigure'">
          <figure style="titre_figure">
            <xsl:apply-templates select="descendant::draw:frame"/>
            <head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a"/>
		</head>
<!--              après le titre [1] : légende -->
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
          </figure>
        </xsl:when>
                <xsl:when test="local-name()='list'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
                  <xsl:when test="local-name()='table'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
        <xsl:when test="@text:style-name='Standard'">
					<p style="txt_Normal">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
        		<xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name">
          			<p style="txt_Normal">
    					<xsl:apply-templates/>
    				</p>
       			</xsl:when>
                 <xsl:when test="@text:style-name='adcontinued-para'">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
                </xsl:when>
                <xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
        		</xsl:when>
				<xsl:when test="@text:style-name='adcitationrom'">
					<quote style="txt_Citation" rend="quotation">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>
        <xsl:when test="@text:style-name='adrecension_5f_titre_5f_biblio'">
          <div type="bibliographie">
            <head style="titre_biblio"><xsl:apply-templates/></head>
            <listBibl>
            <xsl:for-each select="following-sibling::text:p[@text:style-name='adrecension-biblio']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name]">
              <bibl style="txt_Bibliographie"><xsl:apply-templates/></bibl>
            </xsl:for-each>
            </listBibl>
          </div>
        </xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:for-each>
  	</xsl:when>
  	<xsl:otherwise>
  <xsl:for-each select="following-sibling::text:*[preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFull][following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFullSuivante]|following-sibling::text:*[preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]=$recensionFull][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]=$recensionFullSuivante][preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFull][following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFullSuivante]|following-sibling::table:table[preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]=$recensionFull][following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]=$recensionFullSuivante][preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']]">
  	<xsl:choose>
      <xsl:when test="@text:style-name='adtitrefigure'">
        <figure style="titre_figure">
          <xsl:apply-templates select="descendant::draw:frame"/>
            <head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a"/>
		</head>
<!--              après le titre [1] : légende -->
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
          </figure>
      </xsl:when>
         <xsl:when test="local-name()='list'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
          <xsl:when test="local-name()='table'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
    <xsl:when test="@text:style-name='Standard'">
			<p style="txt_Normal">
				<xsl:apply-templates/>
				</p>
		</xsl:when>
    	<xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name">
      		<p style="txt_Normal">
				<xsl:apply-templates/>
			</p>
    	</xsl:when>
         <xsl:when test="@text:style-name='adcontinued-para'">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
                </xsl:when>
                <xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
        		</xsl:when>
		<xsl:when test="@text:style-name='adcitationrom'">
			<quote style="txt_Citation" rend="quotation">
				<xsl:apply-templates/>
			</quote>
		</xsl:when>
    <xsl:when test="@text:style-name='adrecension_5f_titre_5f_biblio'">
      <div type="bibliographie">
        <head style="titre_biblio"><xsl:apply-templates/></head>
        <listBibl>
        <xsl:for-each select="following-sibling::text:p[@text:style-name='adrecension-biblio'][following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFullSuivante]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name][following-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull']=$recensionFullSuivante]">
          <bibl style="txt_Bibliographie"><xsl:apply-templates/></bibl>
        </xsl:for-each>
        </listBibl>
      </div>
    </xsl:when>
		<xsl:otherwise/>
	</xsl:choose>
  </xsl:for-each>
  	</xsl:otherwise>
  	</xsl:choose>
  <xsl:for-each select="following-sibling::text:p[@text:style-name='adauteursect'][preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull'][1]=$recensionFull]|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adauteursect']/@style:name][preceding-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name][1]=$recensionFull]">
    <docAuthor style="auteur_recension">
      <name><xsl:apply-templates/></name>
      <xsl:if test="./following-sibling::text:p[@text:style-name='adinstitution'][1]|./following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name][1]">
        <xsl:for-each select="./following-sibling::text:p[@text:style-name='adinstitution'][1]|./following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name][1]">
          <affiliation style="auteur_recension_institution"><xsl:apply-templates/></affiliation>
        </xsl:for-each>
      </xsl:if>
    </docAuthor>
  </xsl:for-each>
</div>
</xsl:template>

<!-- 1 UE par recension -->
<xsl:template match="text:p[starts-with(@text:style-name,'Titre-recension')]|text:p[@text:style-name=//office:automatic-styles/style:style[starts-with(@style:parent-style-name,'Titre-recension')]/@style:name]">
	<div type="recension">
		<bibl>
			<xsl:apply-templates/>
		</bibl>
<!--
         <xsl:for-each select="following-sibling::table:table">
        <xsl:apply-templates select="." mode="inRecension"/>
        </xsl:for-each>
-->
		<xsl:for-each select="following-sibling::text:*|following-sibling::table:table">
			<xsl:choose>
        <xsl:when test="@text:style-name='adtitrefigure'">
            <figure style="titre_figure">
                		<xsl:apply-templates select="descendant::draw:frame"/>
            <head style="titre_figure">
			<xsl:apply-templates select="text()|text:span|text:a"/>
		</head>
<!--              après le titre [1] : légende -->
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
          </figure>
        </xsl:when>
                <xsl:when test="local-name()='list'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
                <xsl:when test="local-name()='table'">
            <xsl:apply-templates select="." mode="inRecension"/>
                </xsl:when>
        		<xsl:when test="@text:style-name='Standard'">
					<p style="txt_Normal">
						<xsl:apply-templates/>
					</p>
				</xsl:when>
       	 		<xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='Standard']/@style:name">
          			<p style="txt_Normal">
    					<xsl:apply-templates/>
    				</p>
        		</xsl:when>
                 <xsl:when test="@text:style-name='adcontinued-para'">
                     <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
                </xsl:when>
                <xsl:when test="@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adcontinued-para']/@style:name">
	               <p style="txt_Normal_suite">
      	                 <xsl:apply-templates/>
                    </p>
        		</xsl:when>
				<xsl:when test="@text:style-name='adcitationrom'">
					<quote style="txt_Citation" rend="quotation">
						<xsl:apply-templates/>
					</quote>
				</xsl:when>      
				<xsl:when test="@text:style-name='adrecension_5f_titre_5f_biblio' or @text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension_5f_titre_5f_biblio']/@style:name">
					<div type="bibliographie">
						<head style="titre_biblio"><xsl:apply-templates/></head>
            <listBibl>
						<xsl:for-each select="following-sibling::text:p[@text:style-name='adrecension-biblio']|following-sibling::text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adrecension-biblio']/@style:name]">
							<bibl style="txt_Bibliographie"><xsl:apply-templates/></bibl>
						</xsl:for-each>
            </listBibl>
					</div>
				</xsl:when>
				<xsl:when test="@text:style-name='adauteursect'">
					<docAuthor style="auteur_recension">
      					<name><xsl:apply-templates/></name>
      					<xsl:if test="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
          					<xsl:for-each select="following-sibling::text:p[1][@text:style-name='adinstitution']|following-sibling::text:p[1][@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adinstitution']/@style:name]">
            					<affiliation style="auteur_recension_institution"><xsl:apply-templates/></affiliation>
         					 </xsl:for-each>
        				</xsl:if>
					</docAuthor>
				</xsl:when>
				<xsl:otherwise/>
			</xsl:choose>
		</xsl:for-each>
	</div>
</xsl:template>

<!-- fin recension -->

<!-- recension -->

<!-- block
<xsl:template match="text:p[@text:style-name='adouvrage_5f_titre']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_titre']/@style:name]">
    <xsl:variable name="recension" select="."/>
  <div type="recension">
    <bibl>
      <xsl:for-each select="preceding-sibling::text:p[@text:style-name='adouvrage_5f_auteur'][following-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]=$recension]">
        <author style="recension-auteur">
            <xsl:apply-templates/>
        </author>
      </xsl:for-each>
      <title style="recension-titre">
        <xsl:apply-templates/>
      </title>
      <xsl:choose>
          <xsl:when test="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']">
            <date>
              <xsl:value-of select="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][1]/descendant::text:span[@text:style-name='adCAouvrage_5f_date']"/>
            </date>
          </xsl:when>
        <xsl:otherwise/>
      </xsl:choose>
      <xsl:apply-templates select="following-sibling::text:p[@text:style-name='adouvrage_5f_reference'][1]"/>
    </bibl>
    <xsl:for-each select="following-sibling::text:p[@text:style-name='Standard'][preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]=$recension]">
      <p style="txt-recension">
        <xsl:apply-templates/>
      </p>
    </xsl:for-each>
    <xsl:for-each select="following-sibling::text:p[@text:style-name='adauteursect'][preceding-sibling::text:p[@text:style-name='adouvrage_5f_titre'][1]=$recension]">
      <docAuthor style="auteur-recension">
        <name><xsl:apply-templates/></name>
        <xsl:if test="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
          <xsl:for-each select="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
            <affiliation style="auteur-recension-institution"><xsl:apply-templates/></affiliation>
          </xsl:for-each>
        </xsl:if>
      </docAuthor>
    </xsl:for-each>
  </div>
</xsl:template> -->


<!-- inline
<xsl:template match="text:p[@text:style-name='adouvrage_5f_refbibliofull']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_refbibliofull']/@style:name]">
  <xsl:variable name="recensionFull" select="."/>
  <div type="recension">
  <bibl style="biblio-recension">
    <xsl:apply-templates/>
  </bibl>
  <xsl:for-each select="following-sibling::text:p[@text:style-name='Standard'][preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull'][1]=$recensionFull]">
    <p style="txt-recension">
      <xsl:apply-templates/>
    </p>
  </xsl:for-each>
  <xsl:for-each select="following-sibling::text:p[@text:style-name='adauteursect'][preceding-sibling::text:p[@text:style-name='adouvrage_5f_refbibliofull'][1]=$recensionFull]">
    <docAuthor style="auteur-recension">
      <name><xsl:apply-templates/></name>
      <xsl:if test="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
        <xsl:for-each select="./following-sibling::text:p[@text:style-name='adinstitution'][1]">
          <affiliation style="auteur-recension-institution"><xsl:apply-templates/></affiliation>
        </xsl:for-each>
      </xsl:if>
    </docAuthor>
  </xsl:for-each>
</div>
</xsl:template> -->



<!-- auteur de l'ouvrage recensé -->

<xsl:template match="text:p[@text:style-name='adouvrage_5f_auteur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_auteur']/@style:name]">
	<bibl>
		<docAuthor>
			<xsl:apply-templates/>
		</docAuthor>
	</bibl>
</xsl:template>

<xsl:template match="text:p[@text:style-name='adouvrage_5f_auteur']|text:p[@text:style-name=//office:automatic-styles/style:style[@style:parent-style-name='adouvrage_5f_auteur']/@style:name]"/>
    
<!--LISTES-->

<xsl:template match="text:list" mode="inRecension">
    <xsl:variable name="style">
      <xsl:for-each select="key('LISTS',@text:style-name)[1]">
	<xsl:value-of select="@text:style-name"/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:choose>
    <!-- ajout EC -->
    <xsl:when test="descendant::text:p/@text:style-name[contains(., 'puce')]">
    	<list type="unordered">
          <xsl:apply-templates mode="inRecension"/>
        </list>
    </xsl:when>
    <xsl:when test="descendant::text:p/@text:style-name[contains(., 'num')]">
    	<list type="ordered">
          <xsl:apply-templates mode="inRecension"/>
        </list>
    </xsl:when>
    <xsl:when test="descendant::text:p[@text:style-name=//office:automatic-styles/style:style[contains(@style:parent-style-name, 'num')]/@style:name]">
    	<list type="ordered">
          <xsl:apply-templates mode="inRecension"/>
        </list>
    </xsl:when>    
    <!-- fin ajout EC -->
      <xsl:when test="text:list-item/text:h">
	<xsl:for-each select="text:list-item">
	  <xsl:apply-templates mode="inRecension"/>
	</xsl:for-each>
      </xsl:when>
      <xsl:when test="@text:style-name='Var List'">
        <list>
          <xsl:apply-templates mode="inRecension"/>
        </list>
      </xsl:when>
      <xsl:when test="contains($style,'Number')">
        <list type="ordered">
          <xsl:apply-templates mode="inRecension"/>
        </list>
      </xsl:when>
      <xsl:otherwise>
        <list type="unordered">
          <xsl:apply-templates mode="inRecension"/>
        </list>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="text:list-header" mode="inRecension">
      <head>
      <xsl:apply-templates mode="inRecension"/>
    </head>
  </xsl:template>

 <xsl:template match="text:list-item" mode="inRecension">

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
          			<xsl:apply-templates select="." mode="inRecension"/>
        		</xsl:for-each>
      		</item>
    	</xsl:when>
    	<xsl:otherwise>
          <item style="{$styleListe}">
        		<xsl:apply-templates mode="inRecension"/>
      		</item>
    	</xsl:otherwise>
  	</xsl:choose>
</xsl:template>
    
<!--TABLEAUX-->

<xsl:template match="table:table" mode="inRecension">
 
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
              <xsl:apply-templates select="descendant::table:table-cell/*" mode="inRecension"/>
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
</xsl:template>

<xsl:template match="table:table-column" mode="inRecension">
    <xsl:apply-templates mode="inRecension"/>
</xsl:template>

<xsl:template match="table:table-header-rows" mode="inRecension">
    <xsl:apply-templates mode="inRecension"/>
</xsl:template>

<xsl:template match="table:table-header-rows/table:table-row" mode="inRecension">
    <row role="label">
      <xsl:apply-templates mode="inRecension"/>
    </row>
  </xsl:template>

<xsl:template match="table:table/table:table-row" mode="inRecension">
    <row>
      <xsl:apply-templates mode="inRecension"/>
    </row>
</xsl:template>

<!--<xsl:template match="table:table-cell/text:h">
  <xsl:apply-templates/>
</xsl:template> -->


<!-- Modification lourde pour l'ensemble des tableaux : on garde maintenant les paragraphes dans une cellule en désactivant le template suivant !!!!!!À tester!!!!!! Il faut donc utiliser adcellule quand on ne veut pas de structures dans les cellules -->
<!-- <xsl:template match="table:table-cell/text:p">
  <xsl:call-template name="applyStyle"/>
</xsl:template> -->

<xsl:template match="table:table-cell" mode="inRecension">
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
    <xsl:apply-templates mode="inRecension"/>
  </cell>
</xsl:template>

    
</xsl:stylesheet>