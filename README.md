Info for whoever thinks this is for malicious purposes because it contains SQL injection vulnerability results. Those are test cases for my bachelor's work. If you inspect the file contents you will see that the specified URLs for the detected vulnerabilites are mostly IP addresses like 192.168.17.134 or localhost, except for hackazon.lc. It was ip address which I did name for my own testing purposes. If you try to find a site "hackazon.lc" online you will find that it doesn't exist. For more proof of it being ethical hacking I will provide the sources of the testing servers:
1. Hackazon: https://github.com/rapid7/hackazon 
2. Owasp Juice Shop: https://github.com/juice-shop/juice-shop
3. sqli-labs: https://github.com/Audi-1/sqli-labs
4. MCIR (SQLol): https://github.com/SpiderLabs/MCIR
5. Web for Pentesters II: https://www.vulnhub.com/entry/pentester-lab-web-for-pentester-ii,68/

Risinājumu installācijas instrukcijas:
Lai instalētu risinājumu, nepieciešams to ievietot direktorijā "sqlmap/lib/utils". Pēc tam failā "sqlmap/lib/controller/checks.py" jāpievieno atbilstošu importēšanas rindiņu: "from lib.utils.isInjection import isInjection as isInjection", "from lib.utils.isInjection import debug_isInjection as isInjection" vai "from lib.utils.isInjection import clear_isInjection as isInjection", atkarībā no izvēlētā risinājuma. Funkcionālajai un debug versijai papildus jāievieto fails "make_string_equal.py" direktorijā "sqlmap/lib/utils". Kad risinājums ir importēts, rindas no 532. līdz 580. jāaizstāj ar 6.1.1. attēla kodu .

6.1.1. attēls:
![standart_installation.image](images/standart_installation.png)


<h2><b>Testpiemērus tulīt pievienošu pēc vienas studnas. Pagaidām mēģinu tikt galā risinājumu instrukciju rakstīšanu.</b></h2>
