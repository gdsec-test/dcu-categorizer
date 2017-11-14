from iris_helper import IrisHelper
from regex_helper import ListHelper

i = IrisHelper()


def cleanup():
    address = ['sh.baidu.com', 'notices.nr-online.com', 'legal-notification.com', 'woody.ch', 'justdeals.com',
               'certifiedmart.com', 'marcon-media.de', 'newsletter.kopp-verlag.de', 'brandshop.com', 'law360.com',
               'ogrupo.org.br', 'domainerschoice.com', '163.com', 'peakindustry.com', 'woody.ch', 'foxmail.com',
               'sina.cn', 'sina.com', 'appleitunesguide.com', 'notice.bizcn.com']
    garbage = []
    for a in address:
        trash = i.ticket_finder(a)
        for t in trash:
            garbage.append(t[0])

    print garbage


def leomove():
    addresses = ['essex.pnn.police.uk', 'rkn.gov.ru', 'lapd.lacity.org', 'police.midland.on.ca',
                 'montevideopolice.com', 'pcivil.ba.gov.br', 'ccd.gov.eg', 'police.govt.nz', 'pascosheriff.org',
                 'da.lacounty.gov', 'isp.state.il.us', 'cybercrimehelpline.in', 'fremont.gov', 'ksp.policja.gov.pl',
                 'ci.irvine.ca.us', 'ci.kennewick.wa.us', 'walthamforest.gov.uk', 'doj.gov.ph', 'loudoun.gov',
                 'polizei.brandenburg.de', 'comune.roma.it', 'thamesvalley.pnn.police.uk', 'kent.gov.uk',
                 'cra-arc.gc.ca', 'fsa.gov.uk', 'ville.quebec.qc.ca', 'klpd.politie.nl', 'pc.rs.gov.br',
                 'police.london.ca', 'plattsburghpd.com', 'sc.policja.gov.pl', 'michigan.gov', 'polizei.hamburg.de',
                 'dekalbcountyga.gov', 'EBRSO.ORG', 'crispcounty.com', 'calgarypolice.ca', 'riversidesheriff.org',
                 'hampton.gov', 'rcmp-grc.gc.ca', 'police.qld.gov.au', 'acvm-csa.ca', 'fairfield.ca.gov',
                 'border.gov.au', 'rehobothpd.org', 'naplesgov.com', 'ci.eustis.fl.us', 'PeoriaAZ.gov',
                 'limestonecountyda.org', 'south-ayrshire.gov.uk', 'Phila.gov', 'mtnbrook.org', 'portalmedico.org.br',
                 'hudoig.gov', 'jacintocitypd.com', 'ustis.gov', 'manchestertwp.com', 'correo.policia.gov.co',
                 'wiltshire.pnn.police.uk', 'police.ge.ch', 'co.polk.tx.us', 'moi.gov.qa', 'wpb.org',
                 'tspolice.gov.in', 'uttarakhandpolice.uk.gov.in', 'cybercrimeunit.gov.gr', 'fbi.gov', 'cert.gov.pl',
                 'police.sa.gov.au', 'police.go.kr', 'co.price.wi.us', 'netsafe.org.nz', 'MiddletownCTPolice.com',
                 'ca.go.ke', 'policiacivil.sp.gov.br', 'nc3.govt.nz', 'cert.org.cn', 'bis.doc.gov', 'gov.mt',
                 'plainville-ct.gov', 'itransact.co.uk', 'caradonplant.co.uk', 'guardiacivil.org', 'abs.gov.au',
                 'iceweb.net', 'corneliuspd.org', 'aberdeencity.gov.uk', 'asic.gov.au', 'villageoflansing.org',
                 'uk.crimeagency.org', 'police.pref.aichi.lg.jp', 'police.pref.osaka.jp', 'hyd.appolice.gov.in',
                 'hyd.tspolice.gov.in', 'gujarat.gov.in', 'northyorkshire.pnn.police.uk', 'jhpolice.gov.in',
                 'kolkatapolice.gov.in', 'policewb.gov.in', 'CityofRochester.gov', 'leicestershire.pnn.police.uk',
                 'montgomerycountymd.gov', 'avonandsomerset.police.uk', 'fda.hhs.gov', 'oci.fda.gov', 'fca.org.uk',
                 'dbr.ri.gov', 'cheshire.pnn.police.uk', 'doccs.ny.gov', 'finance.gov.ie', 'veterans.idaho.gov',
                 'croydon.gov.uk', 'mail.mil', 'ttu.edu', 'police.tas.gov.au', 'psni.pnn.police.uk',
                 'foodstandards.gsi.gov.uk', 'vpd.ca', 'aitkinpolice.com', 'cns.gob.mx', 'assampolice.gov.in',
                 'delhipolice.gov.in', 'mahapolice.gov.in', 'Police.Saskatoon.Sk.CA', 'LasVegasNevada.GOV',
                 'policiainformatica.gob.pe', 'policia.es', 'irs.gov', 'jcsoky.org', 'ohioattorneygeneral.gov',
                 'pcdf.df.gov.br', 'cityoflondon.police.uk', 'pds.ca', 'bayharborislands.net', 'sao17.state.fl.us',
                 'nr3c.gov.pk', 'forces.gc.ca', 'ci.irs.gov', 'dpf.gov.br', 'milwaukee.gov', 'police.uga.edu',
                 'gov.in', 'truro.ca', 'dany.nyc.gov', 'state.or.us', 'uspis.gov', 'njcu.eduv', 'lstwp.org',
                 'gmp.police.uk', 'rialtopd.com', 'afp.gov.au', 'arjel.fr', 'carabinieri.it', 'poliziadistato.it',
                 'danville.ca.gov', 'surete.qc.ca', 'DODIG.MIL', 'kennemerland.politie.nl', 'fairmont.org',
                 'chesterfield.mo.us', 'pc.mg.gov.br', 'lasd.org', 'guardiacivil.es', 'dcor.state.ga.us',
                 'court.gov.il', 'onet.com.pl', 'met.pnn.police.uk', 'ciaabogados.es', 'torontopolice.on.ca',
                 'sra.org.uk', 'purdue.edu', 'nbi.gov.ph', 'CAMPBELLCOUNTYGOV.COM', 'tarnobrzeg.po.gov.pl',
                 'lantana.org', 'fedpol.admin.ch', 'police.nsw.gov.au', 'boe.ca.gov', 'orkney.gov.uk', 'e-cop.net',
                 'staffordshire.gov.uk', 'doj.state.or.us', 'azag.gov', 'giustizia.it', 'mhra.gsi.gov.uk', 'ct.gov',
                 'police.gov.cy', 'FrederickMDPolice.org', 'forsythco.com', 'sheriff.co.wise.tx.us', 'deity.gov.in',
                 'farmington-ct.org', 'swissnode.ch', 'caixa.gov.br', 'ci.worthington.oh.us', 'desnoix.com',
                 'cornwall.gov.uk', 'rivaldiwebdiensten.nl', 'police.gov.hk', 'ceop.gsi.gov.uk', 'politiet.no',
                 'polizei.bwl.de', 'BrooklynDA.org', 'act.gov.au', 'interieur.gouv.fr', 'lautorite.qc.ca', 'ocsd.org',
                 'kerala.gov.in', 'chirousa.com', 'nominet.org.uk', 'nca.x.gsi.gov.uk', 'madisonvillagepolice.org',
                 'polisen.se', 'justweb.co.jp', 'spf.gov.sg', 'ichaos.me', 'met.police.uk', 'towerhamlets.gov.uk',
                 'axislegal.ca', 'cert-in.org.in', 'nesbit-boeggemeyer.de', 'tci-sit.org', 'polizei.niedersachsen.de',
                 'vspc.appolice.gov.in', 'davidlaw.co.il', 'asqa.gov.au', 'legalforbiz.ro', 'mppolice.gov.in',
                 'nic.in', 'keishicho.jp', 'ihforex.com', 'police.gov.il', 'police.lk', 'derby.gov.uk',
                 'cibercrimen.cl', 'west-midlands.pnn.police.uk', 'MCSO.maricopa.gov', 'politie.nl', 'fcnb.ca',
                 'losgatosca.gov', 'ice.dhs.gov', 'nominet.uk', 'dfs.ny.gov', 'sthelens.gov.uk', 'soca.x.gsi.gov.uk',
                 'usdoj.gov', 'com.state.oh.us', 'tarnow.policja.gov.pl', 'mict.go.th', 'poliisi.fi', 'uscp.gov',
                 'pfes.nt.gov.au', 'doioig.gov', 'rnc.gov.nl.ca', 'politi.dk', 'acgov.org', 'us.af.mil',
                 'northumbria.pnn.police.uk', 'usss.dhs.gov', 'medinaoh.org', 'antifraudcentre.ca',
                 'maplegrovemn.gov', 'rochestermn.gov', 'gamblingcommission.gov.uk', 'brickpd.com', 'bernardspd.org',
                 'lancashire.pnn.police.uk', 'cityoflondon.pnn.police.uk', 'policiacivil.mg.gov.br',
                 'meridiancity.org', 'polizei.nrw.de', 'polizei.bayern.de', 'city-of-london.pnn.police.uk',
                 'oig.dhs.gov', 'police.vic.gov.au', 'peelpolice.ca', 'ic.fbi.gov', 'ontario.ca', 'doj.ca.gov',
                 'durham.pnn.police.uk', 'ccsnypd.org', 'police.somerville.ma.us', 'cityofguthrie.com',
                 'roundrocktexas.gov', 'worcsregservices.gov.uk', 'cyberdept.ru', 'szczecin.pr.gov.pl',
                 'Dyfed-Powys.pnn.policeuk', 'commerce.wa.gov.au', 'camden.gov.uk', 'idoc.IN.gov', 'isp.IN.gov',
                 'unionsheriff.com', 'raleighnc.gov', 'polizei.rlp.de', 'co.gregg.tx.us', 'polizei.landsh.de',
                 'saanichpolice.ca', 'senecacountyso.org', 'hertfordshire.go.uk', 'provo.utah.gov', 'kpf.ca',
                 'pnp.gob.pe', 'wsfc.wa.gov', 'acctrecva.com', 'rpso.la.gov', 'aduana.gob.bo', 'nixi.in',
                 'colegiopetropolis.com', 'leo.gov', 'ci.mt-angel.or.us', 'islington.gov.uk', 'politsei.ee',
                 'cdtfa.ca.gov', 'ky.gov', 'kapo.zh.ch', 'zawiercie.ka.policja.gov.pl', 'policja.gov.pl',
                 'co.stevens.wa.us', 'ekatalog.com.mx', 'laval.ca', 'pnp.gov.ph', 'wyo.gov', 'adpolice.gov.ae',
                 'eastrenfrewshire.gov.uk', 'policija.si', 'policija.lt', 'hants.gov.uk', 'state.de.us',
                 'Dorset.PNN.Police.uk', 'spvm.qc.ca', 'ci.lancaster.oh.us', 'northlan.gcsx.gov.uk', 'northlan.gov.uk',
                 'stirling.gov.uk', 'stirling.gsx.gov.uk', 'co.jefferson.co.us', 'elpasoco.com', 'polizei.sachsen.de',
                 'garda.ie', 'polizei.berlin.de', 'kingcounty.gov', 'fsco.gov.on.ca', 'bmi.gv.at', 'luton.gcsx.gov.uk',
                 'tampagov.net', 'royalgreenwich.gov.uk', 'fccu.be', 'northyorks.gov.uk', 'bcky.org', 'cph.jp',
                 'peoriagov.org', 'ReginaPolice.ca', 'amvic.org', 'cpsc.gov', 'oig.hhs.gov', 'utah.gov',
                 'carmel.in.gov', 'co.dodge.wi.us', 'uwchlan.com', 'moray.gov.uk', 'gsaig.gov', 'detini.gov.uk',
                 'winnipeg.ca', 'fredoniapolice.org', 'pj.pt', 'tamu.edu', 'esafety.gov.au', 'talniri.co.il',
                 'co.orange.tx.us', 'oig.treas.gov', 'majorowen.co.uk', 'tigta.treas.gov', 'cdea.pnn.police.uk',
                 'scotland.pnn.police.uk', 'texasattorneygeneral.gov', 'hampshire.pnn.police.uk', 'danoli.co.uk',
                 'ongov.net', 'jalisco.gob.mx', 'pbso.org', 'dia.govt.nz', 'edmontonpolice.ca', 'hmrc.gsi.gov.uk',
                 'ssp.gob.mx', 'akronohio.gov', 'goapolice.gov.in', 'comune.milano.it', 'alabasterpolice.org',
                 'montrealcitymission.org', 'nterpol.int', 'ssp.cdmx.gob.mx', 'ssp.df.gob.mx', 'yucatan.gob.mx',
                 'guerrero.gob.mx', 'pa.sm', 'gdf.it', 'edinburgh.gov.uk', 'state.mn.us', 'seattle.gov', 'state.gov',
                 'hamiltonpolice.on.ca', 'SuffieldTownHall.com', 'co.merced.ca.us', 'cleveland.pnn.police.uk',
                 'cybercrime.gov.ua', 'dps.usc.edu', 'trumbull-ct.gov', 'mornex.co.il', 'cosource.com.au',
                 'sheriff.org', 'ci.middleton.wi.us', 'tpsgc-pwgsc.gc.ca', 'gendarmerie.interieur.gouv.fr',
                 'jamex.com.mx', 'police.etat.lu', 'glasgow.gov.uk', 'co.chippewa.wi.us', 'ScottsdaleAZ.Gov',
                 'maxnet.ua', 'cert.gov.ng', 'ips.gov.in', 'dbo.ca.gov', 'albertaicenorth.ca', 'Touro.com',
                 'polizei.hessen.de', 'armeco.ca', 'police.brantford.on.ca', 'shillingtonpd.com', 'madrid.es',
                 'mp.gov.in', 'marincounty.org', 'westportct.gov', 'cira.ca', 'cyb.appolice.gov.in', 'egm.gov.tr',
                 'rac.co.uk', 'novascotia.ca', 'manateesheriff.com', 'ahpra.gov.au', 'cbi.gov.in',
                 'grovelandpolice.com', 'lincs.pnn.police.uk', 'gpshoresmi.gov', 'thetownofcicero.com',
                 'bka.bund.de', 'gloucestershire.gov.uk', 'gwent.pnn.police.uk', 'police.wa.gov.au', 'epa.gov',
                 'va.gov', 'heilj.picc.com.cn', 'dorsetcc.gcsx.gov.uk', 'midlandparkpolice.org', 'rpcity.org',
                 'justiciacordoba.gob.ar', 'westmercia.pnn.police.uk', 'dsi.go.th', 'police.be',
                 'polizei.gv.at', 'ncdcr.gov', 'kapo.ai.ch', 'polksheriff.org', 'nottinghamcity.gov.uk', 'gencat.cat',
                 'mail.ci.lubbock.tx.us', 'hennepin.us', 'upstf.com', 'WaucondaPolice.com', 'jus.mendoza.gov.ar',
                 'nordmann-gebler.de', 'ihbarweb.org.tr', 'ssg.gov.ge', 'interno.it', 'flysoft.ru', 'iovon.com',
                 'altatecmonterrey.com', 'pgr.gob.mx', 'westyorkshire.pnn.police.uk', 'maine.gov', 'sunrisefl.gov',
                 'arriendosrenaca.cl', 'bryantx.gov', 'pirst.kr', 'politieherko.be', 'douglascounty-ne.gov',
                 'ventura.org', 'comcom.govt.nz', 'cityoflewisville.com', 'kohlerpolice.com', 'attorneygeneral.gov',
                 'eastdunbarton.gov.uk', 'rsoc.ru', 'royalbijuterii.ro']
    leo = []
    for a in addresses:
        sort = i.ticket_finder(a)
        for t in sort:
            leo.append(t[0])

    print leo


def categorize():

    l = ListHelper()

    phish_keys = ['phishing', 'phish']
    # malware_keys = ['malware', 'virus']
    # netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted']
    # spam_keys = ['spam', 'spoof', 'spoofed']
    # garbage_keys = ['copyright', 'trademark', 'infringement']

    data = [(33289088, u'FRAUD and HARASSMENT that Funds ISIS'),
            (33289417, u'Fraud domain http://www.holdingsbrighton.com'),
            (33290092, u'Fwd: Action required: Please verify your email address/Is someone using my email? Email 4'),
            (33290660, u'Malicious site removal request [3MdEqgRA]'),
            (33290718, u'belgiumbrand.club: SPAM - We need your cooperation'),
            (33290987, u'Abuse: ID THEFT.'),
            (33291012, u'website'),
            (33291117, u'Fraudulent Site'),
            (33291121, u'SPAM /phishing brinksiinc.com'),
            (33291135, u'Phishing at your domain'),
            (33291227, u'RE: Report multiple spear phishing e-mails'),
            (33291235, u'Abuse from 50.62.160.34'),
            (33291241, u'Fw: Important')]

    test = [(123, u'phish'), (456, u'virus'), (789, u'spam'), (012, u'rando')]

    phish_cat = l.reg_logic(test, phish_keys)
    m_list = phish_cat[1]
    phish_cat = phish_cat[0]

    # print i.data_pull()

    # TODO setup regex seperated by category for use in this function

    return phish_cat, m_list

if __name__ == '__main__':
    print categorize()
