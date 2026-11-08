#!/usr/bin/env python3
"""Generate the buildless static guide. Python standard library only."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
('school','天王寺中学校官网','https://swa.city-osaka.ed.jp/j592240','学校位置、最新通知与活动；2026-11-08 核验'),
('district','天王寺区｜2027年度新入学与学校选择制','https://www.city.osaka.lg.jp/tennoji/page/0000656709.html','住址与校区、年度日程及通学规定；2026-11-08 核验'),
('admission','大阪市｜小学、初中入学手续','https://www.city.osaka.lg.jp/kyoiku/page/0000010124.html','外国籍新入学咨询；2026-11-08 核验'),
('size','大阪市｜2025年度学校现况调查','https://www.city.osaka.lg.jp/kyoiku/page/0000659883.html','采用2025-05-01的同日数据，不代表今天人数'),
('sizepdf','三校规模原表｜中学校别班级数、学生数','https://www.city.osaka.lg.jp/kyoiku/cmsfiles/contents/0000659/659883/08_tyugakkobetsugakkyusu_seitosu.pdf','天王寺、高津见PDF第2页，阿倍野见第3页；CC BY 4.0，图表为本站重绘'),
('abeno','阿倍野区｜2027年度学校指南','https://www.city.osaka.lg.jp/abeno/page/0000684952.html','阿倍野中学校介绍及学校选择；2026-11-08 核验'),
('kozu','高津中学校｜毕业去向','https://swa.city-osaka.ed.jp/j592242/page/shinro?tm=20200319164828','官方毕业去向资料入口；不等同三校同口径升学率'),
('events','天王寺中学校｜2025年度行事计划','https://swa.city-osaka.ed.jp/j592240/download/document/15571319?tm=20250716092840','历史活动参考，不作为2026或2027活动日期'),
('culture','天王寺中学校｜2024年区内中学联合文化祭','https://swa.city-osaka.ed.jp/j592240/weblog/117505398?tm=20241217175717','已发生的活动案例；2026-11-08 核验'),
('support','天王寺区｜学业与生活支持者项目','https://www.city.osaka.lg.jp/tennoji/page/0000685560.html','区级项目，不代表各校固定服务时数'),
('hs','大阪府｜2027年度公立高中入学选拔实施要项','https://www.pref.osaka.lg.jp/o180040/kotogakko/gakuji-g3/r09_jisshiyoko.html','含需要日语指导的归国生、外国学生选拔；2026-11-08 核验'),
('bus','大阪City Bus｜中文乘车指南','https://citybus-osaka.co.jp/howto-simplified-chinese/','仅适用于该运营商所列通常乘车方式'),
('bike','大阪市｜防犯要点','https://www.city.osaka.lg.jp/shimin/page/0000370272.html','自行车防犯登记地点'),
('usedbike','大阪市｜二手自行车交接提醒','https://www.city.osaka.lg.jp/joto/page/0000572092.html','确认原登记注销及转让证明'),
('ic','Osaka Metro｜ICOCA','https://subway.osakametro.co.jp/guide/fare/icoca/ICOCA.php','交通卡使用与官方说明'),
]
D={s[0]:s for s in SOURCES}
def ref(k,label='查看官方来源 ↗'):
 return f'<a class="source" href="{D[k][2]}" target="_blank" rel="noopener noreferrer">{label}</a>'
def card(icon,title,body,tag='实用建议',source=None):
 return f'<article class="card searchable"><div class="card-top"><span class="icon" aria-hidden="true">{icon}</span><span class="tag">{tag}</span></div><h3>{title}</h3>{body}'+(ref(source) if source else '')+'</article>'
def grid(*items):return '<div class="grid">'+''.join(items)+'</div>'
def note(title,text):return f'<aside class="notice"><strong>{title}</strong><p>{text}</p></aside>'
def section(n,title,desc=''):return f'<div class="section-heading"><div><span class="eyebrow">{n}</span><h2>{title}</h2></div><p>{desc}</p></div>'
def steps(items):return '<ol class="steps">'+''.join(f'<li><span>{i:02}</span><div><h3>{t}</h3><p>{b}</p></div></li>' for i,(t,b) in enumerate(items,1))+'</ol>'
NAV=[('index.html','指南首页'),('admission.html','入学准备'),('school-life.html','校园日常'),('comparison.html','三校对比'),('high-school.html','高中升学'),('osaka-life.html','大阪生活'),('phrases.html','实用口语')]
PAGES={}
PAGES['index.html']=('从第一天起，\n慢慢熟悉天王寺。','给中国学生与家长的入学、在校和大阪生活指南。把手续理清，把日常过好，也给未来升学留出准备时间。',
'''<div class="hero-actions"><a class="button" href="admission.html">从入学准备开始 <span>↗</span></a><a class="button light" href="comparison.html">看看三校对比 →</a></div>'''+
section('START HERE / 从这里开始','你现在，走到哪一步？','按自己的进度，找到需要的一页。')+
grid(*[f'<a class="card entry" href="{url}"><span class="entry-number">0{i}</span><h3>{title}</h3><p>{body}</p><span class="arrow">↗</span></a>' for i,(url,title,body) in enumerate([('admission.html','正在考虑入学','先确认住址与校区，再了解新入学、转入学和语言支持。'),('school-life.html','准备迎接校园生活','从第一周清单，到体育大会、音乐与文化活动。'),('comparison.html','想看懂学校差异','用同一天的规模数据比较，查看哪些信息仍需询问。')],1)])+
section('A FIRST LOOK / 学校速览','认识大阪市立天王寺中学校','学校官网是校园信息的第一入口。')+
grid(card('校','大阪市立・公立初中','<p>本指南对象为大阪市立天王寺中学校。阅读资料时请核对完整校名，避免混用大阪教育大学附属天王寺中学校的信息。</p>','学校识别','school'),card('地','北河堀町的校园','<p>官网地址：大阪市天王寺区北河堀町6番20号。到访前联系学校，确认预约、来校入口和接待安排。</p>','官网信息','school'),card('572','同日规模参考','<p>2025年5月1日在校生572人，普通班15个。人数是历史截面，更多三校数据见对比页。</p>','2025年度','sizepdf'))+
note('2027年4月新入学：注意当前进度','截至2026年11月8日，天王寺区学校选择希望调查的10月30日提交期限已过。新迁入、漏收通知或错过办理的家庭，请直接向居住区役所咨询，不要等待下一轮网上信息。')+ref('district')+
section('POCKET NOTES / 随手翻一页','先记住这三件小事')+
grid(card('01','不会日语，也要及时求助','<p>把“需要慢一点说明”“希望确认作业”“需要语言支持”直接告诉班主任。把问题写下来，比独自猜测更有效。</p>'),card('02','通学方式先问学校','<p>不要先买通学自行车或交通月票。天王寺区学校选择制的说明列明步行通学、不允许自行车，公共交通原则上禁止，具体适用情况先确认。</p>','通学确认','district'),card('03','看数据，也看适应条件','<p>学校规模不代表教学质量。中文学生人数、日语支持的具体安排与升学率，需要分别核实。</p>')))
PAGES['admission.html']=('把入学手续，\n一步一步理清。','面向外国籍学生家庭。先向居住区确认就学安排，再与学校沟通年级、材料和语言需要。',
note('先确认你的办理类型','“留学生”是本网站的通俗称呼。此处讨论外国籍儿童在市立初中的就学；就学手续、居留资格与高中报考是不同事项，不应互相替代。')+
section('01 / 找到正确路径','新入学与中途转入，分别准备')+
grid(card('春','准备4月进入初一','<p>关注居住区役所发送的入学案内与学校选择说明。没有收到案内，主动询问就学事务窗口。年度期限以居住区通知为准。</p>','大阪市信息','admission'),card('转','从中国或其他地区转入','<p>向居住区役所说明学生年龄、原就读学校、目前年级、预计抵达及住址。请窗口确认适用程序、所需材料和接洽学校，再安排到校。</p>','咨询准备'),card('区','先看住址对应校区','<p>天王寺区按地址确定通学区域校。学校选择制的校外接收有名额限制，比较三校不意味着可以跨区自由入读。</p>','官方规则','district'))+
section('02 / 办理顺序','带着问题去，带着答案回来')+
steps([('联系居住区役所','咨询就学事务窗口，确认校区、办理类型、截止日期，以及是否需要预约或翻译。'),('整理材料，先确认再翻译','准备学生与监护人身份、住址信息、既往就学记录和小学毕业材料供咨询。具体是否需要原件、译文和其他文件，由办理窗口确认。'),('与接收学校面谈','说明日语理解、各科基础、原学校学习内容及健康或过敏等需要。确认年级安排、语言支持和紧急联络方式。'),('领取清单，安排第一天','请学校提供到校时间、用品、服装、午餐、费用说明和通知接收方式。按正式清单采购。')])+
section('03 / 面谈时带上','把语言支持问具体')+
grid(card('语','学生的日语支持','<p>可以询问：是否进行日语水平评估？是否有初期指导或教科学习支持？在哪里上课、每周多久、如何与原班衔接？</p>'),card('家','家长也需要听懂','<p>提前说明希望使用中文或简单日语。询问面谈口译、通知解释、紧急联系渠道是否可以安排，不预设学校配有常驻中文教师。</p>'),card('援','了解区级支持','<p>天王寺区公开募集面向外国背景儿童的学业与生活支持者。家庭可向学校或区役所询问是否有适合的支持安排。</p>','区级项目','support'))+
'<div class="checklist panel"><h2>第一次面谈备忘</h2><p>可勾选后打印；刷新后清空，不上传个人资料。</p>'+''.join(f'<label><input type="checkbox">{s}</label>' for s in ['记录原就读年级与学习情况','写下孩子目前能听懂、能表达的日语','列出所需语言与学习支持','确认上学时间、通学方式及用品','确认通知、请假与紧急联系方法'])+'<button class="button print" type="button">打印这份清单</button></div>')
PAGES['school-life.html']=('在天王寺，\n找到自己的日常。','先熟悉班级，再参与活动。以下区分学校公开活动记录与可直接使用的适应建议。',
section('01 / 校园特色','从公开活动看见学校','历史案例说明活动类型，不保证每年按同样安排举行。')+
grid(card('跑','体育大会：参与整场协作','<p>官网2026年10月发布体育大会实施判断通知。2025年度计划列有班级练习、全体练习、分工碰头和预演，准备过程也是活动的一部分。</p><p class="tip">参与建议：先问自己的项目和分工，留意天气与变更通知。</p>','2025计划 / 2026通知','school'),card('音','音乐竞赛：一起完成一首歌','<p>官网记录2026年三年级音乐竞赛在クレオ大阪中央举行。音乐活动提供课堂之外的共同任务。</p><p class="tip">参与建议：请同学标注歌词读音，确认声部与练习时间。</p>','2026活动记录','school'),card('文','跨校文化交流','<p>2024年天王寺区市立中学联合文化祭中，天王寺中学校的吹奏乐部和合唱部参与跨校联合发表。</p><p class="tip">参与建议：喜欢音乐或作品展示，可在社团介绍时询问活动内容。</p>','2024历史案例','culture'))+
ref('events','查看历史年度活动计划 ↗')+
section('02 / 校园大不同','第一周，把这些小事问明白','以下为一般适应建议，具体以学校规则为准。')+
grid(card('课','作业：除了完成，还要交对','<p>确认作业本、练习册、纸张或数字平台分别怎样提交。记下截止时间、订正要求和忘交后的补交方法。</p>'),card('扫','扫除：看分工，别只扫座位','<p>许多日本学校安排学生参与清扫。到班后问清负责区域、工具与轮值；不把“学校完全没有保洁员”当成固定事实。</p>'),card('鞋','鞋与服装：先拿清单','<p>向学校核实室内鞋、体育馆鞋、标准服、运动服和标名方式。不要仅凭网帖统一购齐。</p>'),card('饭','午餐：有需要提前说','<p>询问午餐提供方式、费用、携带用品和收拾分工。有食物过敏或饮食限制，由监护人提前向学校说明。</p>'),card('部','社团：先体验，再决定','<p>参加部活动介绍，询问训练频率、周末安排、器材费用与请假方法。先考虑自己能否平衡日语学习与体力。</p>'),card('联','请假与通知：家庭一起熟悉','<p>确认请假的时间、渠道与通知接收方式。纸质通知及时交家长；看不懂的截止日期请老师帮忙圈出。</p>'))+
section('03 / 适应节奏','给自己四周时间')+steps([('第1周：敢问','记住班主任、座位、教室、卫生间、保健室和求助方式。'),('第2周：跟上','每天检查作业与通知，建立日中对照的学科词汇本。'),('第3周：参与','找一项能共同完成的任务，例如值日、音乐练习或社团体验。'),('第4周：回顾','与老师和家长讨论仍然困难的场景，把需要的支持说具体。')]))
schools=[{'name':'天王寺中学校','students':572,'classes':15,'supportClasses':6,'grades':[169,212,191]}, {'name':'阿倍野中学校','students':312,'classes':9,'supportClasses':5,'grades':[98,122,92]}, {'name':'高津中学校','students':406,'classes':11,'supportClasses':2,'grades':[154,133,119]}]
(ROOT/'data/schools.json').write_text(json.dumps({'asOf':'2025-05-01','checkedAt':'2026-11-08','source':D['sizepdf'][2],'notes':'生徒数为总数，含特别支援学级学生；普通班与特别支援班分列。中国籍人数、升学率未取得可比公开数据，保留null。','schools':[dict(s,chineseStudents=None,highSchoolProgressionRate=None) for s in schools]},ensure_ascii=False,indent=2)+'\n')
def chart():
 out='<svg class="bar-chart" viewBox="0 0 760 300" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">三校在校生总数对比</title><desc id="chart-desc">2025年5月1日，天王寺572人，阿倍野312人，高津406人。总人数包含特别支援学级学生。</desc>'
 for x,v in [(180,0),(350,200),(520,400),(690,600)]:out+=f'<path d="M{x} 35V255" stroke="#dce3dc"/><text x="{x}" y="285" text-anchor="middle" fill="#68786e" font-size="14">{v}</text>'
 for i,s in enumerate(schools):
  y=55+i*75;w=s['students']/600*510
  out+=f'<text x="8" y="{y+24}" fill="#263f34" font-size="17">{s["name"]}</text><rect x="180" y="{y}" width="{w}" height="38" rx="5" fill="{["#245c47","#739982","#b9cdb3"][i]}"/><text x="{190+w}" y="{y+25}" fill="#263f34" font-size="18" font-weight="700">{s["students"]}</text>'
 return out+'</svg>'
PAGES['comparison.html']=('把学校放在一起，\n把差异看得清楚。','同一统计日期、同一人数口径。规模可以比较，适不适合，还需要到校了解。',
note('三校名称与比较边界','对比对象为大阪市立天王寺中学校、阿倍野中学校、高津中学校；“高京”按前述高津处理。三校涉及不同通学区域，入学可行性须先向居住区确认。')+
section('01 / 规模对比','在校生总数','大阪市教育委员会｜2025年5月1日，非实时人数')+
'<div class="panel">'+chart()+'<p class="caption">单位：人。人数含特别支援学级在籍学生；学校规模不代表教育质量。</p>'+ref('sizepdf')+'</div>'+
'<div class="table-wrap"><table><caption>三校规模明细 · 2025-05-01</caption><thead><tr><th scope="col">指标</th>'+''.join(f'<th scope="col">{s["name"]}</th>' for s in schools)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+label+'</th>'+''.join('<td>'+str(fn(s))+'</td>' for s in schools)+'</tr>' for label,fn in [('在校生总数（人）',lambda s:s['students']),('初一 / 初二 / 初三（人）',lambda s:' / '.join(map(str,s['grades']))),('普通班（个）',lambda s:s['classes']),('特别支援班（个，另列）',lambda s:s['supportClasses']),('中国籍学生人数',lambda s:'未取得可核实公开值'),('高中升学率',lambda s:'未取得同口径数据')])+'</tbody></table></div>'+
section('02 / 数据缺口','中国学生数量与升学率','没有数字的地方，保留真实的空白。')+
grid(card('中','中国学生：先问统计定义','<p>本次所查官方资料未获得三校可比中国籍学生人数。“中文母语”“外国籍”“需要日语指导”并不相同。可询问学校是否有可公开的同年度汇总。</p>','待核实'),card('升','升学率：需要分子和分母','<p>需要同年度毕业生总数、高中等升学人数与统计范围。合格人数可能重复，毕业去向名单也未必完整，不能直接当作升学率。</p>','待核实'),card('六','六个维度，六个问题','<p>规模、语言支持、家校沟通、社团、通学、升学。先用下面的图标清单了解，不凭印象绘制“学校实力”雷达图。</p>','比较方法'))+
section('03 / 看校清单','用六个维度，问到有用的答案')+
grid(*[card(icon,title,f'<p>{body}</p>') for icon,title,body in [('人','学校规模','看同年度总人数与班级数。大校、小校各有体验，实际班级氛围也要了解。'),('语','日语支持','问支持方式、每周时数、与原班课程衔接，以及教科学习支持。'),('家','家校沟通','问中文或简单日语沟通、口译预约，以及紧急联系安排。'),('部','社团活动','问今年实际开设的社团、活动频率、费用和试参加方式。'),('路','通学条件','先查住址对应校区，再确认允许的通学方式和安全路线。'),('升','升学支持','问进路面谈、外国学生报考说明、同年度毕业去向资料。')]])+
'<div class="link-panel">'+ref('abeno','阿倍野区学校指南 ↗')+ref('kozu','高津中学校毕业去向 ↗')+ref('district','天王寺区学校指南 ↗')+'</div>')
PAGES['high-school.html']=('现在的每一点准备，\n都通向下一站。','从适应课堂到准备高中。把学科基础、日语学习和报考条件放进同一张时间表。',
note('三校升学率：当前不列百分比','本次尚未取得三校同年度、同统计范围的毕业人数与实际升学人数。此页提供官方去向入口与准备建议，不以学校学力调查成绩代替升学率。')+
section('01 / 看懂进路信息','去向、合格与升学率，是不同数据')+
grid(card('表','毕业去向可以看什么','<p>先确认年度或累计年数、是否列出所有去向、括号人数含义。高津中学校有官方进路资料入口，可用于了解已公开去向。</p>','官方入口','kozu'),card('率','什么时候才能画升学率图','<p>当三校都公布同年度毕业总人数，以及同定义的实际高中等升学人数时，再计算比例；目前缺失值保持空白，不按0%处理。</p>'),card('路','外国学生相关选拔','<p>大阪府2027年度要项单列“需要日语指导的归国生、外国学生入学者选拔”。国籍本身不保证报考资格，须由学校按具体条件核实。</p>','2027年度','hs'))+
section('02 / 准备时间线','从初一开始，逐渐明确方向','以下是规划建议，不是统一招生日期。')+
steps([('初一：建立学习记录','保持作业与订正习惯，整理中国与日本课程差异；定期与老师回顾日语和教科学习。'),('初二：了解高中类型','在进路面谈中比较课程、通学、费用和支持安排，参加合适的学校说明会。'),('初三上半年：核对资格','向班主任确认适用选拔类别、是否需要事先批准、可申请的考试配虑以及证明材料。'),('初三下半年：按年度要项办理','把志愿、申请、考试和合格后的手续逐项记录。私立、公立及不同类别的日期分别核对。')])+
'<div class="panel"><h2>带去进路面谈的四个问题</h2><ul><li>我符合哪一种选拔的报考条件？</li><li>需要哪些在日学习经历或其他证明？</li><li>是否可以申请日语相关的考试配虑，怎样办理？</li><li>如果第一志愿未录取，后续有哪些实际选择？</li></ul>'+ref('hs','阅读2027年度正式实施要项 ↗')+'</div>')
PAGES['osaka-life.html']=('熟悉一座城市，\n从这些小事开始。','交通、办卡、自行车与生活手续。按实际场景查阅，出门前多确认一步。',
note('上学通勤与日常出行分开看','下列交通卡、公交与自行车内容用于一般生活出行。上学允许的通学方式请先向学校确认，不据此默认可以乘车或骑车上学。')+
section('01 / 交通小卡','坐车之前，先认运营商')+
grid(card('巴','大阪City Bus：下车时付费','<p>按官方通常乘车方式，从后门上车，上车不用取整理券或刷IC卡；到站前按铃，从前门下车时支付车费或刷卡。</p><p class="tip">其他公司、特殊线路可能不同，按该线路标识确认。</p>','运营商规则','bus'),card('卡','交通卡：进出使用同一张','<p>在地铁闸机使用时，进站与出站使用同一张卡或同一设备。先确认余额，遇到闸机提示找站员处理，避免连续换卡尝试。</p><p>ICOCA可用于Osaka Metro及大阪City Bus，具体票种和功能查看官方说明。</p>','出行建议','ic'),card('路','第一次出门，留出余量','<p>记录目的地日文名称、车站出口与返程路线。不要只记“天王寺站”；复杂车站内的步行与换乘也需要时间。</p>'))+
section('02 / 自行车','登记、交接、停车，三件事')+
grid(card('登','买车时询问防犯登记','<p>可在标有“自転車防犯登録所”的自行车销售店办理。购买时请店员说明所需证明与当前费用，并保留购车和登记资料。</p>','大阪市信息','bike'),card('二','二手车先看交接材料','<p>交接前确认原登记注销情况及是否有转让证明。网上买车或朋友赠送也应先向登记店核实手续，别只拿走车钥匙。</p>','官方提醒','usedbike'),card('停','能停的地方，再停','<p>查看停车场标识、使用时段与费用。防犯登记不等于停车许可，也不代表学校允许骑车通学。</p>'))+
section('03 / 家庭一起办理','办卡和生活，不急着一次完成')+
grid(card('通','手机卡：家长一起核对','<p>比较流量、通话、初期费用、合约与解约条件。未成年人申请、支付方式、所需身份材料和设备兼容性，按运营商要求确认。</p>'),card('银','银行卡：按银行清单准备','<p>先向目标银行说明年龄、居住情况与用途，询问监护人是否到场、材料和账户功能。不同机构要求可能不同。</p>'),card('垃','垃圾分类：先找住处规则','<p>向物业或房东确认分类、回收日、指定放置地点与大型垃圾处理。不要把其他城市的垃圾日照搬到大阪住处。</p>'),card('失','遗失物品：记录在哪里丢的','<p>先联系可能遗失地点的车站、公交公司或商店。写下时间、路线和物品特征；向学校求助时可直接展示口语页的句子。</p>')))
phrases=[('课堂求助','もう一度お願いします。','もういちど おねがいします','Mō ichido onegaishimasu','摸—一七多，哦内嘎一西马斯','请再说一遍。','老师、店员；礼貌表达'),('课堂求助','ゆっくり話してください。','ゆっくり はなしてください','Yukkuri hanashite kudasai','优库里，哈那西忒 库达赛','请说慢一点。','老师、不熟悉的人'),('作业确认','いつまでに出せばいいですか。','いつまでに だせば いいですか','Itsu made ni daseba ii desu ka','一词 马得尼，达塞巴 依— 得斯嘎','最晚什么时候交？','向老师确认截止时间'),('扫除分工','何をすればいいですか。','なにを すれば いいですか','Nani o sureba ii desu ka','那尼 哦，斯雷巴 依— 得斯嘎','我应该做什么？','老师、同学；询问任务'),('身体不适','保健室に行ってもいいですか。','ほけんしつに いっても いいですか','Hokenshitsu ni itte mo ii desu ka','厚肯西词 尼，一忒摸 依— 得斯嘎','我可以去保健室吗？','向老师求助'),('同学交流','一緒にやってもいい？','いっしょに やっても いい','Issho ni yatte mo ii?','一秀尼，呀忒摸 依—','我可以一起做吗？','熟悉的同学；随意表达'),('同学交流','それ、どういう意味？','それ どういう いみ','Sore, dō iu imi?','索雷，多—优 意米','那个是什么意思？','同学；不直接用于正式场合'),('请求帮助','ちょっと手伝ってくれる？','ちょっと てつだって くれる','Chotto tetsudatte kureru?','秋托，忒词达忒 库雷鲁','能帮我一下吗？','朋友；随意表达'),('生活求助','忘れ物をしました。','わすれものを しました','Wasuremono o shimashita','哇斯雷摸诺 哦，西马西塔','我落下东西了。','车站或商店工作人员'),('大阪话','ほんま？','ほんま','Honma?','轰马','真的吗？','关西常听到的随意说法'),('大阪话','ええやん。','ええやん','Ee yan','诶—央','挺好的嘛。','朋友间认可；留意语境'),('大阪话','せやな。','せやな','Seya na','塞呀那','是啊。','朋友间回应；正式场合用そうですね')]
PAGES['phrases.html']=('先会说一句，\n就能少慌一点。','课堂、同学和大阪街头常用表达。先学会求助，再慢慢聊得自然。',
note('谐音只作记忆辅助','以假名和罗马音为主要读音参考；中文谐音无法准确表示长音、促音和音调。朋友间的随意说法不直接套用到老师或正式场合。')+
'<label class="search-box" for="phrase-search"><span>⌕</span><input id="phrase-search" type="search" placeholder="查找：作业、老师、大阪话……" aria-label="搜索口语卡片"></label><p id="search-status" class="caption" aria-live="polite">共12条表达，支持搜索中文、日语和罗马音。</p>'+
'<div class="grid phrase-grid">'+''.join(card('言',f'<span lang="ja">{jp}</span>',f'<p lang="ja" class="kana">{kana}</p><p class="roman">{roman}</p><p class="meaning">{meaning}</p><p class="pronunciation">近似谐音：{sound}</p><p class="tip">{use}</p>',cat) for cat,jp,kana,roman,sound,meaning,use in phrases)+'</div><p id="no-results" hidden>暂未找到。试试“求助”“作业”或“大阪话”。</p>')
PAGES['sources.html']=('每一条信息，\n都有来处。','公开来源、统计口径和待补资料。最后核验：2026年11月8日。',
note('独立中文指南','本网站非学校、区役所或招生机构官方网站，不收集学生姓名、联系方式或学习经历。具体办理请查看对应年度官方说明，并向学校或主管部门确认。')+
section('01 / 来源目录','回到原始资料')+'<div class="source-list">'+''.join(f'<article class="source-item" id="{k}"><h3><a href="{url}" target="_blank" rel="noopener noreferrer">{escape(title)} ↗</a></h3><p>{desc}</p></article>' for k,title,url,desc in SOURCES)+'</div>'+
section('02 / 数据说明','哪些是事实，哪些仍需补齐')+
grid(card('数','规模图表','<p>采用大阪市教育委员会2025年5月1日学校现况调查。总人数包含特别支援学级学生，班级数将普通班与特别支援班分列。本站翻译与重绘，原资料按CC BY 4.0署名。</p>'),card('空','缺失值规则','<p>本次公开资料核验未取得三校可比的中国籍学生人数及高中升学率，数据文件保留null。未取得不等于确定未公开，更不等于0。</p>'),card('年','年度与活动','<p>2027年度入学信息、2025年度活动计划与2024年活动报道分别标注。过去活动用于理解校园生活，不作为未来日期承诺。</p>'))+
'<div class="panel"><h2>后续资料更新清单</h2><ul><li>核实三校更近年度、同一天的规模数据。</li><li>查找可公开的中国籍学生汇总及统计定义。</li><li>取得三校同届毕业总人数与实际升学人数。</li><li>补充天王寺当年度校规、作息与活动日历。</li><li>核实日语支持的实际安排与家长咨询渠道。</li></ul><p>不发布可识别个别未成年学生的信息。</p></div>')
for filename,(title,desc,body) in PAGES.items():
 nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if filename==url else '')+f'>{label}</a>' for url,label in NAV)
 ishome=filename=='index.html'
 illustration='''<div class="cover-art" aria-hidden="true"><div class="art-label">OSAKA / TENNOJI<br>STUDENT FIELD NOTES</div><svg viewBox="0 0 400 270" fill="none"><path d="M40 225H360M80 225V90H320V225M65 90L200 30L335 90" stroke="currentColor" stroke-width="3"/><path d="M168 225V169H232V225M104 118H132V144H104ZM158 118H186V144H158ZM214 118H242V144H214ZM268 118H296V144H268ZM104 169H132V195H104ZM268 169H296V195H268Z" stroke="currentColor" stroke-width="2"/><circle cx="200" cy="76" r="15" stroke="currentColor" stroke-width="2"/><path d="M200 65V76L209 81M43 225V156M27 178L43 153L59 178M357 225V148M339 173L357 145L375 173" stroke="currentColor" stroke-width="2"/></svg><div class="art-bottom"><span>大阪市立<br>天王寺中学校</span><b>入学から、その先へ。</b></div><span class="art-sticker">你好，<br>新同学！</span></div>'''
 html=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(desc,quote=True)}"><meta name="theme-color" content="#245c47"><title>{title.replace(chr(10),'')} | 天王寺生活口袋指南</title><link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/css/style.css"><script src="assets/js/main.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><header><div class="header-inner"><a class="brand" href="index.html"><span class="brand-mark">天</span><span>天王寺 · 口袋指南<small>TENNOJI SCHOOL GUIDE</small></span></a><a class="header-source" href="sources.html">非官方指南 <span>↗</span></a></div><nav aria-label="主导航">{nav}</nav></header><main id="main"><div class="breadcrumb"><a href="index.html">大阪生活手册</a><span>/</span>{'开始阅读' if ishome else next((l for u,l in NAV if u==filename),'资料来源')}</div><section class="hero {'home-hero' if ishome else ''}"><div><p class="eyebrow">OSAKA · TENNOJI / 给中国学生与家长</p><h1>{title.replace(chr(10),'<br>')}</h1><p class="intro">{desc}</p><div class="hero-meta"><span class="dot"></span>独立中文指南<span>核验于 2026.11.08</span></div></div>{illustration if ishome else '<div class="page-seal" aria-hidden="true">学<br><span>在大阪，慢慢来。</span></div>'}</section>{body}</main><footer><div><a class="brand" href="index.html"><span class="brand-mark">天</span><span>每一天，多懂一点。</span></a><p>大阪市立天王寺中学校 · 中国学生与家庭生活指南</p></div><div><a href="sources.html">信息来源与数据说明 ↗</a><p>非官方 · 无广告 · 无追踪<br>具体校规、就学与报考以官方通知为准。</p></div></footer></body></html>'''
 (ROOT/filename).write_text(html,encoding='utf-8')
print(f'Generated {len(PAGES)} HTML pages and sourced school dataset.')
