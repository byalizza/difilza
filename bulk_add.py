import requests
import json
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "https://difilza.onrender.com"
ADMIN_KEY = "123456"
TMDB_API_KEY = "69a87754059ce146a5d322ae235a1702"

films_input = """https://www.fullhdfilmizlesene.life/film/yourland-e-yolculuk-journey-to-yourland/ -> https://rapidvid.net/vod/v1xcfe5e965
https://www.fullhdfilmizlesene.life/film/yaz-ortasinda-noel-a-sudden-case-of-christmas/ -> https://rapidvid.net/vod/v1xf072e27f
https://www.fullhdfilmizlesene.life/film/panda-plan-2-the-magical-tribe/ -> https://www.youtube.com/embed/V3jKsgAqFas
https://www.fullhdfilmizlesene.life/film/hui-buh-ve-cadilar-satosu-hui-buh-und-das-hexenschloss/ -> https://rapidvid.net/vod/v1x224ac52f
https://www.fullhdfilmizlesene.life/film/super-mario-galaksi-filmi-the-super-mario-galaxy-movie/ -> https://rapidvid.net/vod/v1x87b8839f
https://www.fullhdfilmizlesene.life/film/motorcu-biker/ -> https://rapidvid.net/vod/v1x62c40f3a
https://www.fullhdfilmizlesene.life/film/yilin-gelini-bruid-van-die-jaar/ -> https://rapidvid.net/vod/v1xf745d99a
https://www.fullhdfilmizlesene.life/film/hoplayanlar-hoppers/ -> https://rapidvid.net/vod/v1xdf8b50cc
https://www.fullhdfilmizlesene.life/film/yerime-gec-swapped/ -> https://rapidvid.net/vod/v1x69a8e622
https://www.fullhdfilmizlesene.life/film/mickey-and-the-very-many-christmases/ -> https://rapidvid.net/vod/v1xe41b338d
https://www.fullhdfilmizlesene.life/film/island-of-lost-girls/ -> https://rapidvid.net/vod/v1x10987b4d
https://www.fullhdfilmizlesene.life/film/acik-hat-on-the-line-1/ -> https://rapidvid.net/vod/v1xbd9d6c24
https://www.fullhdfilmizlesene.life/film/canavarciklar-stitch-head/ -> https://rapidvid.net/vod/v1x92ac5906
https://www.fullhdfilmizlesene.life/film/ayi-teddy-nin-maceralari-teddybjrnens-jul/ -> https://rapidvid.net/vod/v1x180c1f9d
https://www.fullhdfilmizlesene.life/film/the-king-s-daughter/ -> https://rapidvid.net/vod/v1xb1585661
https://www.fullhdfilmizlesene.life/film/kucuk-don-kisot-un-maceralari-giants-of-la-mancha/ -> https://rapidvid.net/vod/v1x9aaec5f2
https://www.fullhdfilmizlesene.life/film/saftirik-greg-in-gunlugu-turunun-son-ornegi-diary-of-a-wimpy-kid-the-last-straw/ -> https://rapidvid.net/vod/v1x2eac305c
https://www.fullhdfilmizlesene.life/film/the-muppet-show/ -> https://rapidvid.net/vod/v1x389517e6
https://www.fullhdfilmizlesene.life/film/sungerbob-korsan-macerasi/ -> https://rapidvid.net/vod/v1x51659859
https://www.fullhdfilmizlesene.life/film/zootopia-2-1-fh/ -> https://rapidvid.net/vod/v1x8e207ad9
https://www.fullhdfilmizlesene.life/film/wicked-for-good/ -> https://www.youtube.com/embed/vt98AlBDI9Y
https://www.fullhdfilmizlesene.life/film/vahsiler-3/ -> https://rapidvid.net/vod/v1x566b9db6
https://www.fullhdfilmizlesene.life/film/gabby-nin-hayal-evi-film/ -> https://rapidvid.net/vod/v1x243419d9
https://www.fullhdfilmizlesene.life/film/sunny-sanskari-ve-tulsi-kumari/ -> https://rapidvid.net/vod/v1x0390ff09
https://www.fullhdfilmizlesene.life/film/aile-terbiyesi/ -> https://rapidvid.net/vod/v1xa3cf0c32
https://www.fullhdfilmizlesene.life/film/kim-demis-kotuyuz-diye-2-3/ -> https://rapidvid.net/vod/v1x354beac9
https://www.fullhdfilmizlesene.life/film/mickey-donald-ve-goofy-uc-silahsorler/ -> https://rapidvid.net/vod/v1x1ccf59ab
https://www.fullhdfilmizlesene.life/film/noel-anne/ -> https://rapidvid.net/vod/v1xce29146e
https://www.fullhdfilmizlesene.life/film/lego-disney-karlar-ulkesi-kutup-martisi-gorevi/ -> https://rapidvid.net/vod/v1xb82ad8b8
https://www.fullhdfilmizlesene.life/film/wayne-ve-lanny-yaramaz-cocuga-karsi/ -> https://rapidvid.net/vod/v1x1f73b82a
https://www.fullhdfilmizlesene.life/film/wayne-ve-lanny-kartopu-operasyonu/ -> https://rapidvid.net/vod/v1xbce497dd
https://www.fullhdfilmizlesene.life/film/dr-seuss-snicler/ -> https://rapidvid.net/vod/v1x22320855
https://www.fullhdfilmizlesene.life/film/cilgin-kopek/ -> https://rapidvid.net/vod/v1x0142e65f
https://www.fullhdfilmizlesene.life/film/ruyalar-diyarinda/ -> https://rapidvid.net/vod/v1x3a135bab
https://www.fullhdfilmizlesene.life/film/daha-cilgin-cuma-1/ -> https://rapidvid.net/vod/v1x790c85b7
https://www.fullhdfilmizlesene.life/film/kiz-canavara-karsi/ -> https://rapidvid.net/vod/v1xcf681053
https://www.fullhdfilmizlesene.life/film/super-charlie/ -> https://rapidvid.net/vod/v1xbd8c3bd7
https://www.fullhdfilmizlesene.life/film/super-ajan-bernard-gorev-mars/ -> https://rapidvid.net/vod/v1xb5b23063
https://www.fullhdfilmizlesene.life/film/harika-kanatlar-maksimum-hiz/ -> https://rapidvid.net/vod/v1x66b8ff29
https://www.fullhdfilmizlesene.life/film/victoria-gitmeli/ -> https://rapidvid.net/vod/v1xcce774a6
https://www.fullhdfilmizlesene.life/film/karate-kid-efsane-dovusculer-2-fh1/ -> https://rapidvid.net/vod/v1x9a238d29
https://www.fullhdfilmizlesene.life/film/parmak-cocuk-emma/ -> https://rapidvid.net/vod/v1xd4ad372b
https://www.fullhdfilmizlesene.life/film/annie-2/ -> https://rapidvid.net/vod/v1xfe166356
https://www.fullhdfilmizlesene.life/film/bay-ve-bayan-kil/ -> https://rapidvid.net/vod/v1x29bc3460
https://www.fullhdfilmizlesene.life/film/leroy-stitch/ -> https://rapidvid.net/vod/v1x94458267
https://www.fullhdfilmizlesene.life/film/cocuk-bakicilarinin-maceralari/ -> https://rapidvid.net/vod/v1xad87bb81
https://www.fullhdfilmizlesene.life/film/caramelo/ -> https://rapidvid.net/vod/v1x47035f25
https://www.fullhdfilmizlesene.life/film/saman-altinda-su/ -> https://rapidvid.net/vod/v1xab66a637
https://www.fullhdfilmizlesene.life/film/inanmalisin-fh/ -> https://www.youtube.com/embed/0r_nbHSOyDE
https://www.fullhdfilmizlesene.life/film/zor-bir-gun/ -> https://rapidvid.net/vod/v1xfe842e76
https://www.fullhdfilmizlesene.life/film/camp-rock-2-buyuk-final/ -> https://rapidvid.net/vod/v1xc4106be5
https://www.fullhdfilmizlesene.life/film/it-s-okay/ -> https://rapidvid.net/vod/v1xc6493d32
https://www.fullhdfilmizlesene.life/film/buyuk-macera-3-cilgin-dostlar/ -> https://rapidvid.net/vod/v1xded0ae15
https://www.fullhdfilmizlesene.life/film/moana-3/ -> https://www.youtube.com/embed/2G5xokNjLK0?si=tFAer59NO2OFqt3K
https://www.fullhdfilmizlesene.life/film/alies-home/ -> https://rapidvid.net/vod/v1xa42c7896
https://www.fullhdfilmizlesene.life/film/yildirim-ailesi-donuyor/ -> https://rapidvid.net/vod/v1xf47a1d47
https://www.fullhdfilmizlesene.life/film/kopek-ve-midilli/ -> https://rapidvid.net/vod/v1x4f343bc9
https://www.fullhdfilmizlesene.life/film/ozi-doganin-koruyucusu/ -> https://rapidvid.net/vod/v1x9d58728b
https://www.fullhdfilmizlesene.life/film/bixler-lisesi-ozel-dedektif/ -> https://rapidvid.net/vod/v1x5d9e71de
https://www.fullhdfilmizlesene.life/film/lego-disney-prenses-kotuler-birlesiyor/ -> https://rapidvid.net/vod/v1x3307f093
https://www.fullhdfilmizlesene.life/film/lego-disney-prenses-kale-macerasi/ -> https://rapidvid.net/vod/v1x047d08ee
https://www.fullhdfilmizlesene.life/film/robin-and-the-hoods/ -> https://rapidvid.net/vod/v1x78f6f31a
https://www.fullhdfilmizlesene.life/film/genc-winnetou-ve-kayip-buffalolar/ -> https://rapidvid.net/vod/v1x94043104
https://www.fullhdfilmizlesene.life/film/tembeller-ailesi/ -> https://rapidvid.net/vod/v1xbe610229
https://www.fullhdfilmizlesene.life/film/dayan-zoey/ -> https://rapidvid.net/vod/v1xd7f91156
https://www.fullhdfilmizlesene.life/film/sut-ve-gol/ -> https://rapidvid.net/vod/v1xed9fa082
https://www.fullhdfilmizlesene.life/film/dahi-cocuk/ -> https://rapidvid.net/vod/v1x65e995da
https://www.fullhdfilmizlesene.life/film/elio-fh/ -> https://rapidvid.net/vod/v1xe8408cab
https://www.fullhdfilmizlesene.life/film/lilo-ve-stic-2-stic-zor-durumda/ -> https://rapidvid.net/vod/v1x186c5e4d
https://www.fullhdfilmizlesene.life/film/lilo-stitch-1/ -> https://rapidvid.net/vod/v1x89031e81
https://www.fullhdfilmizlesene.life/film/stic-filmi/ -> https://rapidvid.net/vod/v1x7f2230aa
https://www.fullhdfilmizlesene.life/film/lilo-ve-stic/ -> https://rapidvid.net/vod/v1xcc4e7fdb
https://www.fullhdfilmizlesene.life/film/ticha-posta/ -> https://rapidvid.net/vod/v1x6bc44bd7
https://www.fullhdfilmizlesene.life/film/dora-sol-dorado-nun-pesinde/ -> https://rapidvid.net/vod/v1x5ce730bf
https://www.fullhdfilmizlesene.life/film/zombiler-4-vampirlerin-safagi/ -> https://rapidvid.net/vod/v1xbce8e5cf
https://www.fullhdfilmizlesene.life/film/dedektif-sun-ve-ekibi-kurtarma-operasyonu/ -> https://rapidvid.net/vod/v1x33873e4d
https://www.fullhdfilmizlesene.life/film/flow-bir-kedinin-yolculugu/ -> https://rapidvid.net/vod/v1x79792a61
https://www.fullhdfilmizlesene.life/film/kayara/ -> https://rapidvid.net/vod/v1x241f3b4b
https://www.fullhdfilmizlesene.life/film/kiz-arkadasim-2/ -> https://rapidvid.net/vod/v1x4e62b4d6
https://www.fullhdfilmizlesene.life/film/kiz-arkadasim/ -> https://rapidvid.net/vod/v1x0d90e7e5
https://www.fullhdfilmizlesene.life/film/young-hearts/ -> https://rapidvid.net/vod/v1x97f233d6
https://www.fullhdfilmizlesene.life/film/k-pop-iblis-avcilari/ -> https://rapidvid.net/vod/v1x528fd3bc
https://www.fullhdfilmizlesene.life/film/karinca-z/ -> https://www.youtube.com/embed/6kqGO1c70ak
https://www.fullhdfilmizlesene.life/film/return-to-wickensburg/ -> https://rapidvid.net/vod/v1x337eb705
https://www.fullhdfilmizlesene.life/film/kopek-adam/ -> https://rapidvid.net/vod/v1xbfc26544
https://www.fullhdfilmizlesene.life/film/pamuk-prenses/ -> https://rapidvid.net/vod/v1xa50a5c57
https://www.fullhdfilmizlesene.life/film/el-dorado-yolu/ -> https://rapidvid.net/vod/v1x764ca2cf
https://www.fullhdfilmizlesene.life/film/noel-baba-3/ -> https://rapidvid.net/vod/v1xe09525e0
https://www.fullhdfilmizlesene.life/film/noel-baba-2/ -> https://rapidvid.net/vod/v1x98ba5fcf
https://www.fullhdfilmizlesene.life/film/noel-baba/ -> https://rapidvid.net/vod/v1x9da2586f
https://www.fullhdfilmizlesene.life/film/die-un-langweiligste-schule-der-welt/ -> https://rapidvid.net/vod/v1x7899faf9
https://www.fullhdfilmizlesene.life/film/lucy-ist-jetzt-gangster/ -> https://rapidvid.net/vod/v1xbd15a1d6
https://www.fullhdfilmizlesene.life/film/niko-kuzey-isiklarinin-otesinde/ -> https://rapidvid.net/vod/v1xf2ef0767
https://www.fullhdfilmizlesene.life/film/100-kurt/ -> https://rapidvid.net/vod/v1xe0c82bad
https://www.fullhdfilmizlesene.life/film/tale-of-the-forest-unicorn/ -> https://rapidvid.net/vod/v1x5aa197ad
https://www.fullhdfilmizlesene.life/film/yolun-basinda-1/ -> https://www.youtube.com/embed/s4aCsaDvagw
https://www.fullhdfilmizlesene.life/film/buyukannem-olmeden-nasil-zengin-olurum/ -> https://rapidvid.net/vod/v1x4d86abc3
https://www.fullhdfilmizlesene.life/film/niko-yildizlara-yolculuk-2/ -> https://rapidvid.net/vod/v1xc41ddd51
https://www.fullhdfilmizlesene.life/film/dounia-et-la-princesse-d-alep/ -> https://rapidvid.net/vod/v1xe3e498ce
https://www.fullhdfilmizlesene.life/film/dalya-ve-kirmizi-kitap/ -> https://rapidvid.net/vod/v1xf684290d
https://www.fullhdfilmizlesene.life/film/desconectados-2-reconectados/ -> https://rapidvid.net/vod/v1xc9d22da0
https://www.fullhdfilmizlesene.life/film/aleksander-ve-felaket-korkunc-berbat-cok-kotu-bir-yolculuk/ -> https://rapidvid.net/vod/v1xe9b8838f
https://www.fullhdfilmizlesene.life/film/ikizler-takimi/ -> https://rapidvid.net/vod/v1xc341d3a6
https://www.fullhdfilmizlesene.life/film/nico-the-unicorn/ -> https://rapidvid.net/vod/v1x6f8fa3ac
https://www.fullhdfilmizlesene.life/film/fisilti-adasi/ -> https://rapidvid.net/vod/v1x9afe2795
https://www.fullhdfilmizlesene.life/film/minik-orumcek-sarlot/ -> https://rapidvid.net/vod/v1x6968f9a1
https://www.fullhdfilmizlesene.life/film/wonderwell/ -> https://rapidvid.net/vod/v1xd330cda6
https://www.fullhdfilmizlesene.life/film/uzaydan-mesaj-var/ -> https://rapidvid.net/vod/v1x0cb3329a
https://www.fullhdfilmizlesene.life/film/evde-tek-basina-6/ -> https://rapidvid.net/vod/v1x041571e1
https://www.fullhdfilmizlesene.life/film/cesur-kanatlar-doganin-sesi/ -> https://rapidvid.net/vod/v1x23f20b27
https://www.fullhdfilmizlesene.life/film/tatil-fiyaskosu/ -> https://rapidvid.net/vod/v1x98b6319d
https://www.fullhdfilmizlesene.life/film/super-maymun-shimmy/ -> https://rapidvid.net/vod/v1xdd182183
https://www.fullhdfilmizlesene.life/film/stinky-summer/ -> https://www.youtube.com/embed/XnCkzzdy7Lg
https://www.fullhdfilmizlesene.life/film/kardan-kiz-kardesim/ -> https://rapidvid.net/vod/v1xe406c315
https://www.fullhdfilmizlesene.life/film/penguen-arkadasim/ -> https://www.youtube.com/embed/BE0kfDCiod0
https://www.fullhdfilmizlesene.life/film/buyuk-miras/ -> https://rapidvid.net/vod/v1x72799ed4
https://www.fullhdfilmizlesene.life/film/merakli-kedinin-10-yasami/ -> https://rapidvid.net/vod/v1xeece7abc
https://www.fullhdfilmizlesene.life/film/le-dernier-jaguar/ -> https://rapidvid.net/vod/v1x46f5b66a
https://www.fullhdfilmizlesene.life/film/asi-prenses/ -> https://rapidvid.net/vod/v1x85d60cf9
https://www.fullhdfilmizlesene.life/film/oyuncaklar-firarda/ -> https://rapidvid.net/vod/v1x70de4c57
https://www.fullhdfilmizlesene.life/film/jurassic-evcil-dinozoru-2/ -> https://rapidvid.net/vod/v1x5b983e11
https://www.fullhdfilmizlesene.life/film/journey-to-the-forbidden-valley/ -> https://rapidvid.net/vod/v1xf6d984e7
https://www.fullhdfilmizlesene.life/film/lassie-yepyeni-bir-macera/ -> https://rapidvid.net/vod/v1x32dfc48b
https://www.fullhdfilmizlesene.life/film/karateci-cocuk-4-fh1/ -> https://rapidvid.net/vod/v1x97be75a3
https://www.fullhdfilmizlesene.life/film/karateci-cocuk-4-yeni-nesil-fh1/ -> https://rapidvid.net/vod/v1xcfe0ff86
https://www.fullhdfilmizlesene.life/film/karateci-cocuk-3-fh1/ -> https://rapidvid.net/vod/v1xedc7e4c3
https://www.fullhdfilmizlesene.life/film/karateci-cocuk-2-fh1/ -> https://rapidvid.net/vod/v1xc6d183ba
https://www.fullhdfilmizlesene.life/film/karateci-cocuk-fh1/ -> https://rapidvid.net/vod/v1xfdefc9f3
https://www.fullhdfilmizlesene.life/film/windstorm-5-buyuk-kasirga/ -> https://rapidvid.net/vod/v1x9197f207
https://www.fullhdfilmizlesene.life/film/kranston-akademi-canavar-bolgesi/ -> https://rapidvid.net/vod/v1xcdc7559b
https://www.fullhdfilmizlesene.life/film/windstorm-4-ari-nin-gelisi/ -> https://rapidvid.net/vod/v1x8fac0075
https://www.fullhdfilmizlesene.life/film/kahraman-hamburgerci/ -> https://rapidvid.net/vod/v1xb78d7665
https://www.fullhdfilmizlesene.life/film/kasirga-3-2/ -> https://rapidvid.net/vod/v1x3712519f
https://www.fullhdfilmizlesene.life/film/kasirga-2/ -> https://rapidvid.net/vod/v1x47ea4ff4
https://www.fullhdfilmizlesene.life/film/kasirga-6/ -> https://rapidvid.net/vod/v1x11e98592
https://www.fullhdfilmizlesene.life/film/marley-ve-ben-2/ -> https://rapidvid.net/vod/v1x2501a3ff
https://www.fullhdfilmizlesene.life/film/me-contro-te-il-film-vacanze-in-transilvania/ -> https://rapidvid.net/vod/v1x0092cb9f
https://www.fullhdfilmizlesene.life/film/pota/ -> https://rapidvid.net/vod/v1x481e5244
https://www.fullhdfilmizlesene.life/film/bak-su-leylege-2-zumrut-tasinin-pesinde/ -> https://rapidvid.net/vod/v1x6b3eb98f
https://www.fullhdfilmizlesene.life/film/bak-su-leylege/ -> https://www.youtube.com/embed/jNJAKIQmpRU
https://www.fullhdfilmizlesene.life/film/altin-gaga-ve-macera-cetesi/ -> https://rapidvid.net/vod/v1xbabacf1a
https://www.fullhdfilmizlesene.life/film/masal-satosu-gizemli-misafir/ -> https://rapidvid.net/vod/v1x1cd1ff27
https://www.fullhdfilmizlesene.life/film/masal-satosu-sihirli-davet/ -> https://rapidvid.net/vod/v1xb9c3bb8a
https://www.fullhdfilmizlesene.life/film/yeni-nesil-kizil-in-yukselisi/ -> https://rapidvid.net/vod/v1x731c5783
https://www.fullhdfilmizlesene.life/film/yeni-nesil-3/ -> https://rapidvid.net/vod/v1x20dc9ba9
https://www.fullhdfilmizlesene.life/film/yeni-nesil-2/ -> https://rapidvid.net/vod/v1x64408010
https://www.fullhdfilmizlesene.life/film/yeni-nesil/ -> https://rapidvid.net/vod/v1x4d75f65d
https://www.fullhdfilmizlesene.life/film/a-greyhound-of-a-girl/ -> https://rapidvid.net/vod/v1xa254b7eb
https://www.fullhdfilmizlesene.life/film/masal-bitti-ben-buyudum-2/ -> https://rapidvid.net/vod/v1x2265e796
https://www.fullhdfilmizlesene.life/film/periler-ulkesi/ -> https://rapidvid.net/vod/v1xa790c986
https://www.fullhdfilmizlesene.life/film/noel-baba-nin-pesinde/ -> https://rapidvid.net/vod/v1xf98dbf5d
https://www.fullhdfilmizlesene.life/film/buz-otelde-dugun/ -> https://rapidvid.net/vod/v1xab9dc284
https://www.fullhdfilmizlesene.life/film/zipir-dedektif-ve-altin-ari-kovani/ -> https://rapidvid.net/vod/v1x5ec2d14a
https://www.fullhdfilmizlesene.life/film/gulliver-in-gezileri/ -> https://rapidvid.net/vod/v1xad1c3f3f
https://www.fullhdfilmizlesene.life/film/me-contro-te-il-film-missione-giungla/ -> https://rapidvid.net/vod/v1x9cccb64b
https://www.fullhdfilmizlesene.life/film/lassie-eve-gel/ -> https://www.youtube.com/embed/5e-ynGfG1ys
https://www.fullhdfilmizlesene.life/film/kucuk-allen-ve-galaksi-yolcusu/ -> https://rapidvid.net/vod/v1xcdc05284
https://www.fullhdfilmizlesene.life/film/cilgin-dostum-finnik/ -> https://rapidvid.net/vod/v1x4ab268a3
https://www.fullhdfilmizlesene.life/film/ayi-kardesler-dunya-ya-donus/ -> https://rapidvid.net/vod/v1xee11ab21
https://www.fullhdfilmizlesene.life/film/agackakan-woody-yaz-kampinda/ -> https://rapidvid.net/vod/v1xd7252d49
https://www.fullhdfilmizlesene.life/film/kahraman-yariscilar/ -> https://rapidvid.net/vod/v1x430bf4ab
https://www.fullhdfilmizlesene.life/film/santaman/ -> https://rapidvid.net/vod/v1xfc68dc71
https://www.fullhdfilmizlesene.life/film/minik-serce/ -> https://rapidvid.net/vod/v1xd48b1855
https://www.fullhdfilmizlesene.life/film/kaptan-porsuk-kayip-hazininin-pesinde/ -> https://rapidvid.net/vod/v1xdf9d9e79
https://www.fullhdfilmizlesene.life/film/barbie-and-stacie-to-the-rescue/ -> https://rapidvid.net/vod/v1xdad7c9af
https://www.fullhdfilmizlesene.life/film/kucuk-buyucu/ -> https://rapidvid.net/vod/v1x44ac5d35
https://www.fullhdfilmizlesene.life/film/yaz-kampina-kacis/ -> https://rapidvid.net/vod/v1x0b3c3116
https://www.fullhdfilmizlesene.life/film/adsiz-kahraman-1/ -> https://rapidvid.net/vod/v1xa22d6102
https://www.fullhdfilmizlesene.life/film/turkey-hollow-kasabasi/ -> https://rapidvid.net/vod/v1x69083ea2
https://www.fullhdfilmizlesene.life/film/buyulu-kahramanlar-buyuk-macera/ -> https://rapidvid.net/vod/v1xbe7052ae
https://www.fullhdfilmizlesene.life/film/belle-ve-sebastian-3-bitmeyen-dostluk/ -> https://rapidvid.net/vod/v1x413b5630
https://www.fullhdfilmizlesene.life/film/sebastian-sevgili-dostum/ -> https://www.youtube.com/embed/DTd8sXijrOw
https://www.fullhdfilmizlesene.life/film/guzel-ve-sebastien/ -> https://www.youtube.com/embed/lsHJK0bgyRw
https://www.fullhdfilmizlesene.life/film/super-aile/ -> https://rapidvid.net/vod/v1xdcfecf1a
https://www.fullhdfilmizlesene.life/film/pinokyo-sihirli-yolculuk/ -> https://rapidvid.net/vod/v1x5236176a
https://www.fullhdfilmizlesene.life/film/80-gunde-devri-alem/ -> https://www.youtube.com/embed/IlsgwJUNFNU
https://www.fullhdfilmizlesene.life/film/findikkiran-ve-sihirli-flut/ -> https://rapidvid.net/vod/v1x0e09b241"""

def extract_title_from_url(url):
    slug = url.rstrip("/").split("/")[-1]
    slug = slug.replace("-fh1", "").replace("-fh2", "").replace("-fh", "").replace("-1", "")
    words = slug.split("-")
    title = " ".join(words).title()
    return title, slug

def search_tmdb(title, slug):
    try:
        clean_title = title.replace(" Ve ", " ve ").replace(" In ", " in ").replace(" Un ", " un ").replace(" Nin ", " nin ")
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(clean_title)}&language=tr-TR"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            year = data["results"][0].get("release_date", "")[:4]
            overview = data["results"][0].get("overview", "")
            original = data["results"][0].get("original_title", "")
            imdb_val = ""

            if poster_path:
                poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                poster = ""

            return {
                "originalTitle": original,
                "year": year,
                "poster": poster,
                "description": overview
            }
    except Exception as e:
        pass

    return {"originalTitle": "", "year": "", "poster": "", "description": ""}

def add_film(title, embed_url, tmdb_data):
    data = {
        "title": title,
        "originalTitle": tmdb_data.get("originalTitle", ""),
        "embedUrl": embed_url,
        "poster": tmdb_data.get("poster", ""),
        "category": "Genel",
        "year": tmdb_data.get("year", ""),
        "imdb": "",
        "description": tmdb_data.get("description", "")
    }

    resp = requests.post(
        f"{API_URL}/api/films",
        json=data,
        headers={"X-Admin-Key": ADMIN_KEY, "Content-Type": "application/json"},
        timeout=10
    )
    if resp.status_code != 201:
        return False, resp.text
    return True, ""

def main():
    lines = [l.strip() for l in films_input.strip().split("\n") if "->" in l and "BULUNAMADI" not in l]

    print(f"Toplam {len(lines)} film eklenecek\n")

    added = 0
    failed = 0

    for i, line in enumerate(lines, 1):
        parts = line.split("->")
        film_url = parts[0].strip()
        embed_url = parts[1].strip()

        title, slug = extract_title_from_url(film_url)

        print(f"[{i}/{len(lines)}] {title} - TMDB araniyor...")
        tmdb_data = search_tmdb(title, slug)

        if tmdb_data.get("originalTitle"):
            print(f"  -> {tmdb_data['originalTitle']} ({tmdb_data.get('year', '?')})")

        success, err = add_film(title, embed_url, tmdb_data)
        if success:
            print(f"  -> Eklendi!")
            added += 1
        else:
            print(f"  -> HATA: {err[:100]}")
            failed += 1

        time.sleep(0.3)

    print(f"\n{'='*40}")
    print(f"Tamamlandi! {added} eklendi, {failed} basarisiz")

if __name__ == "__main__":
    main()
