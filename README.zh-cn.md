# cli-anyweb

鎶婁换鎰忕綉绔欏彉鎴愭洿閫傚悎 Agent 浣跨敤鐨?CLI銆?
`cli-anyweb` 鏄竴涓熀浜?Vercel Labs `agent-browser` 鐨勬祻瑙堝櫒 harness 涓庢彃浠跺寲宸ヤ綔娴侊紝鐩爣鏄妸涓轰汉绫昏璁＄殑缃戠珯閫愭杞寲涓?Agent 鍙皟鐢ㄣ€佸彲澶嶇敤銆佸彲璇勪及鐨勫懡浠ゅ紡鎿嶄綔闈€?
[English](./README.md) | 绠€浣撲腑鏂?
涓€鍙ヨ瘽姒傛嫭锛氶€氳繃缁撴瀯鍖栨祻瑙堝櫒鎺у埗銆佺珯鐐?reference銆佸彲鍥炴斁璺緞鍜?eval 鏈哄埗锛屾妸鏅€?Web 杞欢鍙樻垚鏇撮€傚悎 Agent 浣跨敤鐨勫伐鍏枫€?
## 瀹冩槸浠€涔?
`cli-anyweb` 鐢变笁灞傜粍鎴愶細

- 涓€涓€氱敤娴忚鍣?harness锛屽簳灞傚熀浜?`agent-browser`
- 涓€濂楃敤浜庢湭鐭ョ綉绔欐帴鍏ャ€乫low 鍙戠幇涓庤矾寰勬矇娣€鐨勬柟娉曡
- 涓€涓被浼?`cli-anything-plugin` 鐨勬彃浠剁粨鏋勶紝璁╂瘡涓綉绔欓兘鑳芥湁鑷繁鐨?setup銆乺eference 涓?eval 璧勪骇

## 蹇€熷鑸?
- [蹇€熷紑濮媇(#蹇€熷紑濮?
- [涓轰粈涔堣繖浠朵簨閲嶈](#涓轰粈涔堣繖浠朵簨閲嶈)
- [涓轰粈涔堜笉鐩存帴鐢?agent-browser](#涓轰粈涔堜笉鐩存帴鐢?agent-browser)
- [浠撳簱缁撴瀯](#浠撳簱缁撴瀯)
- [璺嚎鍥綸(#璺嚎鍥?
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)
- [ROADMAP.md](./ROADMAP.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)

## 鐥涚偣

浠婂ぉ鐨勫ぇ妯″瀷宸茬粡鍏峰寰堝己鐨?GUI 鎿嶄綔鑳藉姏锛宍agent-browser` 杩欑被宸ュ叿涔熻娴忚鍣ㄦ帶鍒舵洿瀹规槗鎺ュ叆銆?
浣嗏€滆兘鎿嶄綔鈥濆苟涓嶇瓑浜庘€滈€傚悎闀挎湡绋冲畾鍦颁綔涓?Agent 鍩虹璁炬柦鏉ヤ娇鐢ㄢ€濄€?
鍦ㄧ湡瀹炰换鍔￠噷锛屽緢澶氭ā鍨嬩緷鐒朵細鍦ㄧ綉椤甸噷鍙嶅鈥滈殢鏈烘父璧扳€濓細

- 姣忔杩愯閮借閲嶆柊瀵绘壘鐩稿悓鐨勬搷浣滆矾寰?- 閲嶅鑺辫垂 token 鍜屾椂闂村幓瀹氫綅宸茬粡鎵捐繃鐨勬寜閽€佽彍鍗曞拰娴佺▼
- 鍗充娇浠诲姟鑳藉畬鎴愶紝涔熶笉涓€瀹氭槸鏈€楂樻晥銆佹渶绋冲畾銆佹渶鍙鐢ㄧ殑鏂瑰紡

瀵逛簬鏈€寮虹殑 SOTA 妯″瀷锛岃繖绉嶄綆鏁堟湁鏃惰繕鑳芥帴鍙楋紱浣嗗浜庢洿灏忋€佹洿渚垮疁銆佹垨鏇翠笓鐢ㄧ殑妯″瀷锛岃繖绉嶆崯鑰椾細鏇存槑鏄俱€?
鐪熸缂哄皯鐨勶紝涓嶅彧鏄祻瑙堝櫒鎺у埗鑳藉姏锛岃€屾槸涓€灞傚彲绉疮銆佸彲澶嶇敤銆佸 Agent 鍙嬪ソ鐨勪氦浜掑熀纭€璁炬柦锛岃 Web 涓嶅啀鏄瘡娆￠兘瑕侀噸鏂版帰绱㈢殑鐜锛岃€屾槸閫愭笎鍙樻垚绋冲畾鍙潬鐨勫伐鍏烽潰銆?
## 鎰挎櫙

`cli-anyweb` 甯屾湜甯姪鏋勫缓 Agent 鍘熺敓鐨?Web 鐢熸€侊細

- 鏃犻棬妲涙帴鍏ワ細浠讳綍缃戠珯閮藉彲浠ラ€氳繃缁撴瀯鍖?CLI 绔嬪埢琚?Agent 鎿嶆帶
- 鏃犵紳闆嗘垚锛氫笉闇€瑕佷笓闂?API銆佷笉闇€瑕佽瑙夐€氶亾椹卞姩 GUI銆佷笉闇€瑕侀噸鏋勪唬鐮侊紝涔熶笉闇€瑕佸鏉傞€傞厤灞?- 闈㈠悜鏈潵锛氱綉绔欏彲浠ラ€愭鍙樻垚 Agent 鐨勫彲澶嶇敤宸ュ叿锛岃€屼笉鏄竴娆℃涓村満鎺㈢储鐨勭幆澧?
## 涓轰粈涔堣繖浠朵簨閲嶈

濡傛灉 Web 瑕佺湡姝ｆ垚涓?Agent 鐨勬墽琛岀幆澧冿紝閭ｄ箞鎴愬姛灏变笉鑳戒緷璧栤€滄瘡娆￠兘閲嶆柊璧颁竴閬?UI鈥濄€?
鍏抽敭杞彉鍦ㄤ簬锛?
- 浠庝竴娆℃€х殑娴忚鍣ㄦ帶鍒?- 鍒板彲澶嶇敤鐨?Web 宸ヤ綔娴?- 鍐嶅埌鍙瘎浼般€佸彲鎸佺画浼樺寲鐨勭珯鐐圭煡璇?
杩欐鏄繖涓粨搴撴兂琛ヤ笂鐨勯偅涓€灞傘€?
## 涓轰粈涔堜笉鐩存帴鐢?`agent-browser`

`agent-browser` 鏄繖閲岀殑鍩虹锛岃€屼笖瀹冩湰韬凡缁忔彁渚涗簡寰堝己鐨勬祻瑙堝櫒鎺у埗鑳藉姏銆?
浣嗕粎鏈夆€滄帶鍒舵祻瑙堝櫒鈥濆苟涓嶈兘瑙ｅ喅鏇撮珮涓€灞傜殑 Agent 闂锛?
- 鑳芥帶鍒讹紝涓嶇瓑浜庢湁鍙鐢ㄧ殑宸ヤ綔娴佺粨鏋?- 鑳藉畬鎴愪竴娆′氦浜掞紝涓嶇瓑浜庢湁绋冲畾鐨勮矾寰勫彂鐜拌兘鍔?- 涓€娆℃垚鍔熻繍琛岋紝涓嶇瓑浜庡舰鎴愪簡浼氭寔缁Н绱€佹寔缁敼杩涚殑 Web 鎿嶄綔灞?
`cli-anyweb` 鎯宠ˉ涓婄殑锛屽氨鏄繖涓€灞傦細

- 鏇撮€傚悎 Agent 閲嶅璋冪敤鐨勭粨鏋勫寲 CLI 鍛戒护闈?- 姣旂函瑙嗚椹卞姩鏇磋交閲忋€佹洿绋冲畾鐨?snapshot 妫€鏌ュ師璇?- 鍙矇娣€绔欑偣缁忛獙鐨?references锛岄伩鍏嶆瘡娆￠兘浠庡ご鍙戠幇璺緞
- 鍙洖鏀俱€佸彲璇勪及銆佸彲鎸佺画浼樺寲鐨?replay/eval 鏀拺
- 鍙负鍏蜂綋缃戠珯瀹氫箟 setup 涓庢祻瑙堝櫒瑕佹眰鐨?plugin 缁撴瀯

鍙互绠€鍗曠悊瑙ｄ负锛歚agent-browser` 鎻愪緵娴忚鍣ㄨ兘鍔涳紝鑰?`cli-anyweb` 璇曞浘鎶婅繖绉嶈兘鍔涘彉鎴愨€滀换鎰忕綉绔欑殑鍙鐢?CLI鈥濄€?
## 鏍稿績鎬濊矾

瀹冪殑鏍稿績闂幆寰堢畝鍗曪細

1. 閫氳繃缁撴瀯鍖栨祻瑙堝櫒 harness 鎵撳紑骞舵鏌ョ綉绔?2. 鎵惧埌涓€鏉″彲琛岀殑浜や簰璺緞
3. 鎶婅繖鏉¤矾寰勬矇娣€鎴愬彲澶嶇敤鐨?Agent 鐭ヨ瘑
4. 鎸佺画鍥炴斁銆佽瘎浼板苟杩唬浼樺寲

杩欐牱锛學eb 浜や簰灏变笉鍐嶆槸涓€娆℃閲嶅鎺㈢储锛岃€屼細閫愭笎鍙樻垚涓€涓彲绉疮鐨勭郴缁熴€?
## 宸ヤ綔娴?
```text
Open -> Inspect -> Act -> Capture -> Reuse -> Evaluate
```

鏇村叿浣撲竴鐐癸細

- `open`锛氭墦寮€鐩爣椤甸潰
- `snapshot` / `ls` / `cat` / `grep` / `find`锛氭鏌ュ綋鍓嶄氦浜掗潰
- `click` / `type`锛氭墽琛屼氦浜掕矾寰?- references锛氭妸鎴愬姛璺緞娌夋穩涓嬫潵
- evals锛氬綋绔欑偣鍙樺寲鏃讹紝鍥炴斁骞惰瘎浼拌繖浜涜矾寰?- plugin setup锛氫负鍏蜂綋缃戠珯瀹氫箟鐪熷疄 UA銆佹祻瑙堝櫒 flags 绛変笓灞炶姹?
## 瀹夎

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## 蹇€熷紑濮?
```bash
cli-anyweb open https://example.com
cli-anyweb snapshot
cli-anyweb find Example
cli-anyweb get url
```

褰撳墠 CLI 閲囩敤鎵佸钩鍛戒护闈紝渚嬪 `open`銆乣snapshot`銆乣ls`銆乣click`銆乣find`銆?
## 浣犱細寰楀埌浠€涔?
- 鎵佸钩銆侀€傚悎 Agent 璋冪敤鐨勬祻瑙堝櫒鍛戒护
- 鍩轰簬 snapshot 鐨勭粨鏋勫寲妫€鏌ヤ笌璺緞瀹氫綅
- 鍙繚瀛樼珯鐐?reference 涓庡彲澶嶇敤 flow 鐭ヨ瘑鐨勭洰褰曠粨鏋?- 閫氬線 replay銆乪valuation 涓庢寔缁紭鍖栫殑宸ヤ綔娴?- 鍙负鍏蜂綋缃戠珯鎵╁睍 setup 鐨?plugin 灞?
## 浠撳簱缁撴瀯

- [setup.py](./setup.py)
- [agent_harness/README.md](./agent_harness/README.md)
- [agent_harness/skills/SKILL.md](./agent_harness/skills/SKILL.md)
- [agent_harness/skills/references](./agent_harness/skills/references)
- [agent_harness/skills/evals](./agent_harness/skills/evals)
- [agent_harness/tests/TEST.md](./agent_harness/tests/TEST.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)
- [references](./references)
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)

## 璺嚎鍥?
- 鍐冲畾鏄惁灏嗗唴閮ㄥ寘鐩綍浠?`agent_harness` 閲嶅懡鍚嶄负 `cli_anyweb`
- 缁х画娓呯悊鍘嗗彶鍛藉悕涓庡亸 filesystem 椋庢牸鐨勯仐鐣欒〃杩?- 澧炲姞 `example.com` 涔嬪鐨勭湡瀹炵珯鐐?references
- 寤虹珛妯″瀷椹卞姩璺緞鍙戠幇鐨?replay/eval 闂幆
- 鎵╁睍 backend 鐩稿叧娴嬭瘯
- 璁?site-specific plugin setup 鎴愪负涓€绛夎兘鍔?
鏇村畬鏁寸殑鎵ц璁″垝瑙?[ROADMAP.md](./ROADMAP.md)銆?
## 閰嶇疆

- 鎺ㄨ崘鍖呭悕锛歚cli-anyweb`
- 鎺ㄨ崘 CLI 鍛戒护锛歚cli-anyweb`
- 鎺ㄨ崘棰濆娴忚鍣ㄥ弬鏁扮幆澧冨彉閲忥細`CLI_ANYWEB_AGENT_BROWSER_FLAGS`
- 褰撳墠鍐呴儴鍖呰矾寰勬殏鏃朵粛涓?`agent_harness`

## 涓轰粈涔堣繖涓粨搴撹鐙珛鍑烘潵

杩欎釜浠撳簱鏈€鍒濇槸浠庢洿澶х殑 `CLI-Anything` 浣撶郴閲屾媶鍑烘潵鐨勪竴涓祻瑙堝櫒 harness銆?
鐜板湪瀹冩鍦ㄨ閲嶆柊缁勭粐鎴愪竴涓洿鏄庣‘鐨勬柟鍚戯細

- 鎻愪緵閫氱敤娴忚鍣?harness
- 鎻愪緵绫讳技 `cli-anything-plugin` 鐨勬彃浠剁粨鏋?- 璁╄础鐚€呭彲浠ユ妸浠绘剰缃戠珯閫愭杞垚鍙鐢ㄧ殑绔欑偣 CLI

铏界劧瀵瑰浜у搧鍚嶅凡缁忓垏鍒?`cli-anyweb`锛屽綋鍓?Python 鍖呬粛鏆傛椂鏀惧湪浠撳簱鏍圭洰褰曚笅鐨?`agent_harness/`銆?
## 鑷磋阿涓庡綊灞?
杩欎釜椤圭洰缁ф壙骞跺弬鑰冧簡浠ヤ笅宸ヤ綔锛?
- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- `cli-anything-plugin/HARNESS.md` 涓殑鏂规硶璁?- 鍘熷娴忚鍣?harness 鐨勫疄鐜版€濊矾
- 鍚庣画琚縼绉诲苟閫傞厤鍒?`agent-browser` 鐨勬墦鍖呯粨鏋勩€丷EPL 绾﹀畾鍜?backend 闆嗘垚鏂瑰紡

`cli-anyweb` 鏄熀浜?`CLI-Anything` 鐨勪粨搴撶粨鏋勪笌 harness 鏂规硶鏁寸悊鍑烘潵鐨勮鐢熼」鐩€?
鍦ㄦ枃妗ｃ€佸彂甯冭鏄庛€侀暅鍍忔垨瀵瑰浠嬬粛涓紝搴旂户缁繚鐣欏涓婃父椤圭洰鐨勬竻鏅板綊灞炶鏄庛€?
