
// UK Proxy PAC file for all countries using UKProxy with standard exceptions
/*  This is the main function called by any browser */
function FindProxyForURL(url, host)
{
//start of gtld
if (shExpMatch(host, "*.hsbc")) {
  if (shExpMatch(host, "*.uk.hsbc") ||
      shExpMatch(host, "*.fr.hsbc")) 
   return "DIRECT";

  if (shExpMatch(host, "*.adroot.hsbc") ||
      shExpMatch(host, "*.adroot1.hsbc") ||
      shExpMatch(host, "*.adres.hsbc") ||
      shExpMatch(host, "*.uk.hsbc") ||
      shExpMatch(host, "*.hk.hsbc") ||
      shExpMatch(host, "*.us.hsbc") ||
	  shExpMatch(host, "*.qa.hsbc") ||
      shExpMatch(host, "*.global.hsbc") ||
      shExpMatch(host, "*.ad.hsbc") || 
      shExpMatch(host, "*.hbeu.hsbc") ||
      shExpMatch(host, "*.hibm.hsbc") ||
      shExpMatch(host, "*.mx.hsbc"))
    return "DIRECT";

  var doms = ["ad","addev","adres","adroot","adroot1","adroottest","ae","am","ar","asiapacific","au","bd","be","bh","bm","bn","br","bronze","bs","ca","ch","chan","ck","cl","cn","co","cr","cy","cz","de","dotcom","dz","eg","es","europe","fr","ge","ghq","global","globalduediligence","gmo","gold","gold-QTcont","gold-QTlive","gr","gt","hbeu","hibm","hk","hn","hsbcnet","hsstax","hsstaxHK","hsstaxHK-QTcont","hsstaxHK-QTlive","hsstax-QTcont","hsstax-QTlive","id","ie","il","in","internal","it","jp","kr","kw","ky","kz","jo","latinamerica","lb","lk","lu","mc","middleeast","mo","movi","mt","mu","mv","mx","my","ni","nl","nz","om","pa","je","pe","ph","pk","pl","ps","ptsecurities","py","qa","ru","sa","sg","silver","silver-cont","silver-QTcont","silver-QTlive","sv","th","tr","tw","ua","uk","us","uy","vn","za","zinc","zinc-QTcont","zinc-QTlive"];

  for (i=0; i < doms.length; i++) {
    var teststr = ".".concat(doms[i],".hsbc");

     if (~host.indexOf(teststr))
      return "DIRECT";

   }
     return "PROXY uk-proxy-01.systems.uk.hsbc:80";
  }
//end of gtld

/* List of exceptions for direct access */
    if (isPlainHostName(host) ||                                    // No Proxy for Non FQDN names
    shExpMatch(host, "127.0.0.1") ||                                // No Proxy for LocalHost
    shExpMatch(host, "flashservice.adobe.com") ||                   // No Proxy for Adobe Flash 12 plugin
    dnsDomainIs(host, ".session.rservices.com") ||                  // No Proxy for rservices.com Extranet 
    dnsDomainIs(host, ".cp.thomsonreuters.net") ||                  // No Proxy for cp.thomsonreuters.net 
    dnsDomainIs(host, ".extranet.thomsonreuters.biz") ||            // No Proxy for extranet.thomsonreuters.biz CR380710
    dnsDomainIs(host, ".extranet.reuters.biz") ||                   // No Proxy for extranet.reuters.biz 
    dnsDomainIs(host, ".trading.thomsonreuters.net") ||             // No Proxy for trading.thomsonreuters.net 
    dnsDomainIs(host, "portalsbe.redbde.es") ||                     // No proxy for portalsbe.redbde.es - Spain local users to Bank of Spain Portal
    dnsDomainIs(host, "fedtradesoftware.federalreserve.org") ||     // No Proxy for Federal Trade Application in Extranet
    dnsDomainIs(host, "fedtradeprod.federalreserve.org") ||         // No Proxy for Federal Trade Application in Extranet 
    dnsDomainIs(host, "fedtradesoftwareprod.federalreserve.org") || // No Proxy for Federal Trade Application in Extranet
    dnsDomainIs(host, "taapsdlrqa.treasuryauction.gov") ||          // No Proxy for Federal Trade Application in Extranet
    dnsDomainIs(host, "taapsdlr.treasuryauction.gov") ||            // No Proxy for Federal Trade Application in Extranet 
    dnsDomainIs(host, "client.kontiki.com"))                        // No Proxy for client.kontiki.com for kontiki client specific

      return "DIRECT";
	  
    if (dnsDomainIs(host, ".eu2.kontiki.com"))  
      return "PROXY uk-proxy-kontiki.systems.uk.hsbc:80";

    if (shExpMatch(url, "*www.research.hsbc.com/*"))
      return "PROXY uk-proxy-sy.systems.uk.hsbc:80";
	  
    if (dnsDomainIs(host, ".morganstanley.com"))
      return "PROXY gbsyh152bg020-old.systems.uk.hsbc:80";

    if (shExpMatch(url, "*sp.morganstanley.com/*"))
      return "PROXY gbsyh152bg020-old.systems.uk.hsbc:80";	
	  
    if (dnsDomainIs(host, ".ironport.com"))                      // Cisco anyconnect unneccesary background traffic sent to localhost
      return "PROXY 127.0.0.1:18080";

    if (dnsDomainIs(host, ".fnz.net") ||                         // FNZ redirect to SY
        dnsDomainIs(host, ".fnz.co.uk"))
      return "PROXY uk-proxy-sy.systems.uk.hsbc:80";

    if (dnsDomainIs(host, ".firstdataclients.eu"))               // Firstdata redirect to SY
      return "PROXY uk-proxy-sy.systems.uk.hsbc:80";

    if (dnsDomainIs(host, "hsbc.dealogic.com"))                         // IN32271911 redirect to wdc
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";

    if (dnsDomainIs(host, "rsapps-dev.hsbc.co.uk"))                         // IH-[21042017][IN33375378][redirect to wdc]
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";

    if (dnsDomainIs(host, "ms.m4.net"))                         // IH-[21042017][for D.Hawkes]
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";
  	  
    if (dnsDomainIs(host, ".futuresdirect.hsbcnet.com") ||                         
        dnsDomainIs(host, ".europe.futuresdirect.hsbc.com") ||
	dnsDomainIs(host, "usercenter.checkpoint.com") ||
	dnsDomainIs(host, "ondemand.ca.com"))
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";
   
    if (dnsDomainIs(host, "swppvtapps.gws.seic.com"))
      return "PROXY nhq-app-proxy-sy.systems.uk.hsbc:80";           //IH-[25012018][SEIC timeout issues]

    if (dnsDomainIs(host, "swift-euro1-iws.swiftnet.sipn.swift.com"))  // SWIFT Download issue via SY
	  return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";

	if (shExpMatch(url, "swift-euro1-iws.swiftnet.sipn.swift.com/*"))
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";

    if (dnsDomainIs(host, "traders.liquidnet.com"))
      return "PROXY 128.12.24.250:80";

    if (dnsDomainIs(host, "etfmanager.source.info"))
      return "PROXY GBSYH152BG020-lan.systems.uk.hsbc:80";
	
    if (dnsDomainIs(host, "portal02.intelligentdataconnections.com"))
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";

    if (shExpMatch(url, "*portal02.intelligentdataconnections.com/*"))
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";	

    if (dnsDomainIs(host, "liquidity-management.hsbcnet.com") ||  
        dnsDomainIs(host, "liquidity-management-preprod.hsbcnet.com") ||  
        dnsDomainIs(host, "iquidity-management-dev.hsbcnet.com"))     
      return "PROXY uk-proxy-wdc.systems.uk.hsbc:80";	 
    
    if (dnsDomainIs(host, "prd.impact.spsfi.broadridge.com") ||   // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "uat.impact.spsfi.broadridge.com") ||   // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "prd.spsfi.broadridge.com") ||          // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "uat.spsfi.broadridge.com") ||          // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "gcasxq.broadridge.com") ||             // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "gcasx.broadridge.com") ||              // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "gcasxq-app.broadridge.com") ||         // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "gcasx-app.broadridge.com") ||          // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "secureqa.spsnet.broadridge.com") ||    // NY GBM Proxy for Broadridge services
        dnsDomainIs(host, "secure.spsnet.broadridge.com"))        // NY GBM Proxy for Broadridge services

      return "PROXY GBM-Proxy.us.hsbc:8080";

    if (dnsDomainIs(host, ".world-television.com") ||
	dnsDomainIs(host, ".live.edgefcs.net") ||
        dnsDomainIs(host, ".streamzilla.xlcdn.com")) {
		if (isInNet(myIpAddress(), "128.19.0.0", "255.255.0.0") ||
		    isInNet(myIpAddress(), "128.25.0.0", "255.255.0.0") ||
		    isInNet(myIpAddress(), "128.26.64.0", "255.255.255.0") ||
		    isInNet(myIpAddress(), "128.26.96.0", "255.255.255.0") ||
		    isInNet(myIpAddress(), "128.30.0.0", "255.255.0.0")) {
      return "PROXY uk-proxy-sy.systems.uk.hsbc:80";
	} else {
	return "PROXY uk-proxy-01.systems.uk.hsbc:80";
            } 
     }

//access to t2s swiftnet - used by French back office

if( shExpMatch( url, "*t2s-*.ssp.swiftnet.sipn.swift.com*" ) && !shExpMatch( url, "*t2s-*-proxy.ssp.swiftnet.sipn.swift.com*")){
return "PROXY 127.0.0.1:18080";
}

   return "PROXY uk-proxy-01.systems.uk.hsbc:80";
} 

