#!/usr/bin/env python3
"""Generates the static, bilingual (EN/AR) Nora AlSaud site into ./site.

Content below is taken from the captured website (see docs/AUDIT.md). Nothing here is
invented: counts are derived from the captured service list / project categories, and every
contact detail comes from the captured Contact pages.
"""
import json, html, datetime, os, shutil, stat

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = f'{ROOT}/site'
BASE = 'https://noraengineers.com'          # production origin used for canonicals / hreflang / schema
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year
MAN = json.load(open(f'{ROOT}/tools/manifest.json'))

PAGES = ['home', 'about', 'services', 'projects', 'careers', 'contact']
SERV_SLUGS = ['architecture', 'interiors', 'furniture', 'identity', 'landscape', 'supervision']
PATH = {
    'ar': {'home': '/', 'about': '/about/', 'services': '/services/', 'projects': '/projects/', 'careers': '/careers/', 'contact': '/contact/',
           **{f'service_{s}': f'/services/{s}/' for s in SERV_SLUGS}},
    'en': {'home': '/en/', 'about': '/en/about/', 'services': '/en/services/', 'projects': '/en/projects/', 'careers': '/en/careers/', 'contact': '/en/contact/',
           **{f'service_{s}': f'/en/services/{s}/' for s in SERV_SLUGS}},
}
PHONE_TEL = '+966138966727'
PHONE_DISP = '+966 13 896 6727'
EMAIL = 'info@noraengineers.com'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Jarir+Plaza+Prince+Turki+Street+Khobar'

# ---------------------------------------------------------------- icons
def svg(path, cls='', extra=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false" {extra}>{path}</svg>'
ARROW = svg('<path d="M4 12h15M13 6l6 6-6 6"/>', 'arrow')
UP = svg('<path d="M12 19V5M6 11l6-6 6 6"/>', 'up')
SUN = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>', 'ico ico-sun')
MOON = svg('<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>', 'ico ico-moon')
CLOSE = svg('<path d="M6 6l12 12M18 6L6 18"/>')
CHEV = svg('<path d="M9 5l7 7-7 7"/>')
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4.5v15a.8.8 0 0 0 1.2.7l12-7.5a.8.8 0 0 0 0-1.4l-12-7.5A.8.8 0 0 0 7 4.5z"/></svg>'

e = html.escape

# ---------------------------------------------------------------- content
SERV_SLUGS = ['architecture', 'interiors', 'furniture', 'identity', 'landscape', 'supervision']

C = {
'en': dict(
    lang='en', dir='ltr', locale='en_US', other='ar',
    name='Nora AlSaud Architects & Engineers', short='Nora AlSaud', sub='Architects & Engineers',
    alt_name='Nora Engineers',
    nav={'home': 'Home', 'about': 'About', 'services': 'Services', 'projects': 'Projects', 'careers': 'Join us', 'contact': 'Contact'},
    switch='العربية', switch_label='عرض الموقع بالعربية',
    ui=dict(skip='Skip to content', menu='Menu', primary_nav='Primary', mobile_nav='Mobile', theme='Dark mode', btt='Back to top', lang_switch='Language',
            view_projects='View projects', our_services='Our services', all_services='All services', all_projects='All projects',
            home='Home', open_maps='Open in Maps', required='Required', send='Send message', apply='Submit application', optional='optional',
            close='Close', prev='Previous image', next='Next image', rail_prev='Scroll projects back', rail_next='Scroll projects forward',
            play='Play the office film', related='See related projects', gallery='Project gallery', filter='Filter projects',
            all='All', residential='Residential', commercial='Commercial', showing='Showing',
            service_eyebrow='Service', view_service='View service details', deliv_eyebrow='Deliverables',
            deliv_heading='Key deliverables & scope', deliv_lede='Concrete design packages and technical documentation delivered with precision.',
            proc_eyebrow='Methodology', proc_heading='How we deliver this discipline', proc_lede='A disciplined, four-stage progression from brief to completion.'),
    i18n=dict(demo="This is a preview. The form isn't connected to a server yet, so nothing has been sent.",
              fix='Please complete the highlighted required fields.', sent='Thank you. Your message has been sent.',
              failed="Sorry, we couldn't send your message. Please email us directly.", fileBig='File must be 5 MB or smaller.', showing='Showing'),
    meta={
        'home': ('Nora AlSaud Architects & Engineers | Khobar, Saudi Arabia',
                 'Engineering and design office in Khobar offering architecture, interiors, furniture design, identity & branding, landscape, and project supervision & execution.'),
        'about': ('About Us | Nora AlSaud Architects & Engineers',
                  'Meet Nora AlSaud Architects & Engineers: an engineering office with considerable experience and a lot of passion, turning client vision into space and form.'),
        'services': ('Services: Architecture, Interiors, Landscape | Nora AlSaud',
                     'Architecture, interiors, furniture design, identity & branding, landscape, and supervision & execution: six design and delivery services from one office in Khobar.'),
        'projects': ('Projects: Residential & Commercial Design | Nora AlSaud',
                     'A gallery of residential and commercial interior projects, shown as design visualisations, by Nora AlSaud Architects & Engineers.'),
        'careers': ('Join Us | Nora AlSaud Architects & Engineers',
                    'Want to work with Nora AlSaud Architects & Engineers? Send your details and portfolio through our application form.'),
        'contact': ('Contact | Nora AlSaud Architects & Engineers, Khobar',
                    'Contact our office in Khobar, Prince Turki Street, Jarir Plaza: phone, email, location and working hours (Sunday to Thursday).'),
        'service_architecture': ('Architectural Design Services | Nora AlSaud Architects & Engineers',
                                 'Comprehensive architectural design for residential and commercial projects in Saudi Arabia, from concept to execution drawings.'),
        'service_interiors': ('Interior Design Services | Nora AlSaud Architects & Engineers',
                              'Tailored interior design for residential and commercial spaces: spatial flow, 3D visualisations, lighting, and premium material palettes.'),
        'service_furniture': ('Custom Furniture Design | Nora AlSaud Architects & Engineers',
                              'Custom-crafted furniture and artisan joinery tailored to individual spaces, balancing spatial scale, ergonomic comfort, and architectural elegance.'),
        'service_identity': ('Identity & Environmental Branding | Nora AlSaud Architects & Engineers',
                             'Visual brand identity, spatial signage, packaging, and wayfinding systems designed to elevate commercial environments and build lasting recognition.'),
        'service_landscape': ('Landscape Architecture & Outdoor Design | Nora AlSaud Architects & Engineers',
                              'Harmonious landscape architecture and outdoor living design connecting architectural volumes with nature, climate-responsive planting, and curated hardscape.'),
        'service_supervision': ('Project Supervision & Execution Management | Nora AlSaud Architects & Engineers',
                                'Comprehensive site supervision, material quality control, and schedule management protecting fidelity to approved architectural designs.'),
    },
    address='Khobar, Prince Turki Street, Jarir Plaza, Second Floor, Office 203',
    country='Saudi Arabia',
    hours='8:00 AM – 5:00 PM', days='Sunday – Thursday',
    hero=dict(eyebrow='Architects & Engineers · Khobar',
              h1='It’s all about <em>architecture</em>, engineering, design &amp; art.',
              lede='An engineering office that listens to your vision and shapes it into space, form and mass.',
              cap_k='Residential', cap_v='Bedroom · design visualisation'),
    facts=[('6', 'Disciplines under one roof'), ('2', 'Project categories: residential & commercial'), ('Khobar', 'Prince Turki Street'), ('Sun–Thu', '8:00 AM – 5:00 PM')],
    intro=dict(eyebrow='The office', stmt='An engineering office with <em>considerable experience</em> and a lot of passion.',
               p='We provide engineering and design services at a high level of professionalism and reliability. We listen to our clients’ vision and concepts and transform them into area, space and mass.',
               vision_k='Our vision', vision='Create a renewed, creative architectural environment that reflects on society and affects it positively.'),
    svc=dict(eyebrow='What we do', h='Six disciplines, from first idea to site.', lede='Architecture, interiors, furniture, identity, landscape and project delivery, all shaped by one design line.'),
    work=dict(eyebrow='Selected work', h='Residential interiors and commercial spaces.', lede='Shown as design visualisations: the way a space is imagined, detailed and presented to the client.'),
    process=dict(eyebrow='How we work', h='From listening to delivery.'),
    film=dict(eyebrow='Office film', h='A look inside the office.', p='A short walkthrough of our office.'),
    cta=dict(h='Have a project <em>in mind</em>?', p='Tell us about your space and what you need from it.', a='Contact us', b='Join the team'),
    footer=dict(blurb='Engineering and design services for residential and commercial projects, from our office in Khobar.', explore='Explore', visit='Visit', hours='Working hours', rights='All rights reserved.'),
),
'ar': dict(
    lang='ar', dir='rtl', locale='ar_SA', other='en',
    name='نورة السعود معماريون ومهندسون', short='نورة السعود', sub='معماريون ومهندسون',
    alt_name='Nora AlSaud Architects & Engineers',
    nav={'home': 'الرئيسية', 'about': 'من نحن', 'services': 'خدماتنا', 'projects': 'مشاريعنا', 'careers': 'انضم إلينا', 'contact': 'اتصل بنا'},
    switch='English', switch_label='View the site in English',
    ui=dict(skip='تخطَّ إلى المحتوى', menu='القائمة', primary_nav='الرئيسية', mobile_nav='الجوال', theme='الوضع الداكن', btt='العودة إلى الأعلى', lang_switch='اللغة',
            view_projects='استعرض المشاريع', our_services='خدماتنا', all_services='جميع الخدمات', all_projects='جميع المشاريع',
            home='الرئيسية', open_maps='افتح في الخرائط', required='مطلوب', send='إرسال الرسالة', apply='تقديم الطلب', optional='اختياري',
            close='إغلاق', prev='الصورة السابقة', next='الصورة التالية', rail_prev='تمرير المشاريع للخلف', rail_next='تمرير المشاريع للأمام',
            play='تشغيل فيديو المكتب', related='شاهد المشاريع ذات الصلة', gallery='معرض المشاريع', filter='تصفية المشاريع',
            all='الكل', residential='سكنية', commercial='تجارية', showing='عدد المشاريع المعروضة',
            service_eyebrow='الخدمة', view_service='استعراض تفاصيل الخدمة', deliv_eyebrow='المخرجات',
            deliv_heading='نطاق العمل والمخرجات', deliv_lede='حزم تصميمية وتنفيذية متكاملة تُسلَّم بأعلى درجات الدقة الهندسية.',
            proc_eyebrow='منهجية العمل', proc_heading='كيف نقدّم هذه الخدمة', proc_lede='مسار عمل هندسي من أربع مراحل ينقل المشروع من الفكرة إلى التنفيذ.'),
    i18n=dict(demo='هذه نسخة تجريبية. النموذج غير مرتبط بخادم بعد، لذلك لم يتم إرسال أي شيء.',
              fix='يرجى إكمال الحقول المطلوبة المحددة.', sent='شكراً لك، تم إرسال رسالتك.',
              failed='عذراً، تعذّر إرسال رسالتك. يرجى مراسلتنا عبر البريد الإلكتروني.', fileBig='يجب ألا يتجاوز حجم الملف 5 ميجابايت.', showing='عدد المشاريع المعروضة'),
    meta={
        'home': ('نورة السعود معماريون ومهندسون | الخبر، المملكة العربية السعودية',
                 'مكتب هندسي في الخبر يقدّم التصميم المعماري والداخلي وتصميم الأثاث والهوية والحدائق، إضافةً إلى الإشراف والتنفيذ.'),
        'about': ('من نحن | نورة السعود معماريون ومهندسون',
                  'تعرّف على مكتب نورة السعود معماريون ومهندسون: خبرة مهنية وشغف، نحوّل رؤية العميل إلى مساحة وفراغ وكتلة.'),
        'services': ('خدماتنا: عمارة وتصميم داخلي وحدائق | نورة السعود',
                     'التصميم المعماري والداخلي، وتصميم الأثاث والهوية والحدائق، والإشراف والتنفيذ: ست خدمات هندسية وتصميمية من مكتب واحد في الخبر.'),
        'projects': ('مشاريعنا: تصاميم سكنية وتجارية | نورة السعود',
                     'معرض لمشاريع داخلية سكنية وتجارية على شكل تصورات تصميمية من نورة السعود معماريون ومهندسون.'),
        'careers': ('انضم إلينا | نورة السعود معماريون ومهندسون',
                    'ترغب بالعمل مع نورة السعود معماريون ومهندسون؟ أرسل بياناتك ونماذج من أعمالك عبر نموذج التقديم.'),
        'contact': ('اتصل بنا | نورة السعود معماريون ومهندسون، الخبر',
                    'تواصل مع مكتبنا في الخبر، شارع الأمير تركي، جرير: الهاتف والبريد الإلكتروني والموقع وساعات العمل (من الأحد إلى الخميس).'),
        'service_architecture': ('خدمات التصميم المعماري | نورة السعود معماريون ومهندسون',
                                 'تصميم معماري متكامل للمشاريع السكنية والتجارية في الخبر والمملكة العربية السعودية، من دراسة الفكرة إلى المخططات التنفيذية.'),
        'service_interiors': ('خدمات التصميم الداخلي | نورة السعود معماريون ومهندسون',
                              'تصميم داخلي متكامل للمساحات السكنية والتجارية: مخططات وظيفية، تصورات ثلاثية الأبعاد، وتنسيق دقيق للمواد والإضاءة.'),
        'service_furniture': ('تصميم الأثاث المخصص | نورة السعود معماريون ومهندسون',
                              'تصميم وتفصيل قطع أثاث حصرية تلائم الفراغات المعمارية وتلبي متطلبات الاستخدام بأعلى معايير الجودة والأناقة.'),
        'service_identity': ('تصميم الهوية والعلامة التجارية | نورة السعود معماريون ومهندسون',
                             'بناء وتطوير الهوية البصرية، تصميم الشعارات والتغليف والتطبيقات المكانية المتوافقة مع الروح المعمارية للمشروع.'),
        'service_landscape': ('تصميم الحدائق والمساحات الخارجية | نورة السعود معماريون ومهندسون',
                              'تصميم حدائق ومساحات خارجية متكاملة تبني تناغماً بين الطبيعة والكتلة المعمارية والجلسات التفاعلية.'),
        'service_supervision': ('الإشراف والتنفيذ وإدارة المشاريع | نورة السعود معماريون ومهندسون',
                                'إدارة ومتابعة دقيقة لمراحل التنفيذ في الموقع، وضبط الجودة والجدول الزمني لضمان مطابقة المنفذ للتصميم المعتمد.'),
    },
    address='المملكة العربية السعودية، الخبر، شارع الأمير تركي، جرير، الدور الثاني، مكتب 203',
    country='المملكة العربية السعودية',
    hours='8:00 صباحاً – 5:00 مساءً', days='الأحد – الخميس',
    hero=dict(eyebrow='معماريون ومهندسون · الخبر',
              h1='كل شيء يدور حول <em>العمارة</em> والهندسة والتصميم والفن.',
              lede='مكتب هندسي يُنصت إلى رؤيتك ويحوّلها إلى مساحة وفراغ وكتلة.',
              cap_k='سكني', cap_v='غرفة نوم · تصور تصميمي'),
    facts=[('6', 'تخصصات في مكتب واحد'), ('2', 'فئتان للمشاريع: سكنية وتجارية'), ('الخبر', 'شارع الأمير تركي'), ('الأحد–الخميس', '8:00 ص – 5:00 م')],
    intro=dict(eyebrow='عن المكتب', stmt='مكتب هندسي بـ<em>خبرة مهنية ثرية</em> وشغف كبير.',
               p='نقدّم الخدمات الهندسية والتصميمية على مستوى عالٍ من الاحترافية والدقة. نستمع لعملائنا ونقرأ تطلعاتهم لإخراجها في المساحة والفراغ والكتلة.',
               vision_k='رؤيتنا', vision='تشكيل بيئة عمرانية إبداعية متجددة تنعكس بدورها على المجتمع وتؤثر فيه إيجاباً.'),
    svc=dict(eyebrow='ماذا نقدّم', h='ست خدمات، من الفكرة الأولى إلى الموقع.', lede='العمارة والتصميم الداخلي والأثاث والهوية والحدائق والإشراف على التنفيذ، ضمن توجّه تصميمي واحد.'),
    work=dict(eyebrow='من أعمالنا', h='مساحات سكنية داخلية وأماكن تجارية.', lede='معروضة كتصورات تصميمية: الطريقة التي تُتخيَّل بها المساحة وتُفصَّل وتُقدَّم للعميل.'),
    process=dict(eyebrow='كيف نعمل', h='من الإصغاء إلى التنفيذ.'),
    film=dict(eyebrow='فيديو المكتب', h='جولة داخل المكتب.', p='جولة قصيرة في مكتبنا.'),
    cta=dict(h='هل لديك مشروع <em>في بالك</em>؟', p='حدّثنا عن مساحتك وما تحتاجه منها.', a='تواصل معنا', b='انضم إلى الفريق'),
    footer=dict(blurb='خدمات هندسية وتصميمية للمشاريع السكنية والتجارية من مكتبنا في الخبر.', explore='استكشف', visit='زيارتنا', hours='ساعات العمل', rights='جميع الحقوق محفوظة.'),
),
}

SERV = {
 'en': {
  'architecture': ('Architecture', 'Architectural design for every type of project (residential, commercial and other uses), shaped around the client’s needs and requirements and our own design line.'),
  'interiors': ('Interiors', 'Interior design for residential, commercial and other projects: from schematic design and 3D visuals to materials selection, balancing function with beauty.'),
  'furniture': ('Furniture design', 'Turning imagination and inspiration into pieces that follow our design line, fit the space and meet the client’s needs.'),
  'identity': ('Identity & branding', 'Creating and developing logos, packaging and product design that support the growth of the client’s project and sit naturally within its space.'),
  'landscape': ('Landscape', 'Landscape and outdoor seating design that builds harmony between people and place, reinforcing the strong relationship between landscape and architectural mass.'),
  'supervision': ('Supervision & execution', 'Full monitoring and control of the project: analysing scope, available resources and timing, with a complete and detailed report to the client to protect quality and fidelity to the design.'),
 },
 'ar': {
  'architecture': ('التصميم المعماري', 'تصميم معماري متكامل للمشاريع بمختلف أنواعها (السكنية والتجارية وغيرها)، وفق احتياجات العميل ومتطلباته ضمن توجّهنا التصميمي.'),
  'interiors': ('التصميم الداخلي', 'تصميم داخلي للمشاريع السكنية والتجارية وغيرها، يجمع بين الوظيفة والروح الجمالية: من التصميم التخطيطي والرسومات ثلاثية الأبعاد إلى اختيار المواد.'),
  'furniture': ('تصميم الأثاث', 'تشكيل قطع أثاث تترجم فكرة التصميم بطريقة وظيفية تلائم المكان، وفق توجّهنا التصميمي واحتياج العميل.'),
  'identity': ('تصميم الهوية', 'إنشاء وتطوير الشعار والعلامة التجارية وتصميم العبوات والمنتجات، بما يدعم نمو مشروع العميل ويتجانس مع تصميم المكان.'),
  'landscape': ('تصميم الحدائق', 'تصميم الحدائق والجلسات الخارجية بما يبني الانسجام والتناغم بين المستخدم والمكان، مع التأكيد على العلاقة القوية بين تصميم الحدائق والتصميم المعماري.'),
  'supervision': ('الإشراف والتنفيذ', 'إدارة ومراقبة المشروع بالكامل: تحليل نطاق العمل والموارد المتاحة والجدول الزمني، مع تقرير كامل ومفصل للعميل حرصاً على جودة التنفيذ ومطابقته للتصميم.'),
 },
}

STEPS = {
 'en': [('Listen', 'We start with the client’s vision, concepts, needs and requirements.'),
        ('Concept', 'Exchanging ideas and presenting the initial design idea.'),
        ('Schematic design', 'Developing the layout and planning of the space.'),
        ('3D visuals & materials', 'Bringing the design to life in 3D and selecting materials.'),
        ('Execution drawings', 'Producing the drawings needed to build the design.'),
        ('Supervision & execution', 'Monitoring scope, resources and timing, with detailed reporting to the client.')],
 'ar': [('الإصغاء', 'نبدأ برؤية العميل وأفكاره واحتياجاته ومتطلباته.'),
        ('الفكرة المبدئية', 'تبادل الأفكار وتقديم الفكرة التصميمية المبدئية.'),
        ('التصميم التخطيطي', 'تطوير التخطيط وتوزيع المساحات.'),
        ('الرسومات ثلاثية الأبعاد والمواد', 'تجسيد التصميم بالأبعاد الثلاثية واختيار المواد.'),
        ('الرسومات التنفيذية', 'إعداد الرسومات اللازمة لتنفيذ التصميم.'),
        ('الإشراف والتنفيذ', 'مراقبة النطاق والموارد والوقت، مع تقارير مفصلة للعميل.')],
}

SERV_DETAIL = {
 'en': {
  'architecture': dict(
    h1='Architecture & <em>Master Planning</em>.',
    lede='Comprehensive architectural design for residential, commercial, and mixed-use projects, shaped around the client’s lifestyle and our distinctive architectural language.',
    overview_h='Architecture responding to place, light, and living.',
    p1='At Nora AlSaud Architects & Engineers, architectural design is the synthesis of spatial intelligence, structural integrity, and aesthetic poise. We believe that architecture must respond to its cultural and climatic context in Saudi Arabia while providing functional flexibility and timeless visual dignity.',
    p2='From initial site orientation and massing studies to building permit coordination and municipal approvals, our Khobar studio guides clients through every phase of building design. We translate complex functional briefs into cohesive structural forms with considered daylighting, generous spatial volume, and enduring materials.',
    badge='Architectural Blueprint & Schematic Model',
    ref='NAS-ARC-01',
    deliv=[
      ('01', 'Concept Massing & Zoning', 'Comprehensive solar orientation, circulation logic, and volumetric studies tailored to site conditions and client requirements.'),
      ('02', 'Schematic Architectural Design', 'Detailed 3D floorplans, elevations, and volumetric models exploring interior-exterior relationships.'),
      ('03', 'Construction Documentation', 'Full architectural drawing sets, structural and MEP coordination, and detailed architectural specifications.'),
      ('04', 'Permitting & Code Compliance', 'Rigorous alignment with the Saudi Building Code (SBC) and municipal authority approval submissions.'),
    ],
    steps=[
      ('Site & Context Analysis', 'Analyzing topography, solar angles, access points, and municipal zoning regulations.'),
      ('Massing & Concept Design', 'Exploring spatial configurations, scale, proportions, and architectural character.'),
      ('Detail Development', 'Integrating engineering disciplines, refining building envelopes, and selecting architectural materials.'),
      ('Technical Documentation', 'Delivering comprehensive working packages, tender sets, and municipal permit documentation.'),
    ],
  ),
  'interiors': dict(
    h1='Interior Design & <em>Spatial Styling</em>.',
    lede='Interior architecture for residential villas, luxury apartments, and commercial venues, uniting functional ergonomics with refined atmospheres.',
    overview_h='Crafting lived environments with warmth and discipline.',
    p1='Our interior design service approaches interior spaces as lived experiences. We shape volume, light, acoustic balance, and tactile surfaces into environments that feel both welcoming and profoundly curated. Every layout is calibrated to how our clients move, gather, and rest.',
    p2='By integrating bespoke joinery, carefully orchestrated lighting scenarios, and exquisite natural materials—from travertine and walnut to brushed bronze—we deliver spaces of effortless sophistication. We work closely with our clients from schematic layouts to on-site styling.',
    badge='Interior Perspective & Lighting Specification',
    ref='NAS-INT-01',
    deliv=[
      ('01', 'Spatial Layout & Circulation', 'Strategic space planning that maximizes room flow, functional zones, and natural lighting.'),
      ('02', 'Photorealistic Visualisations', '3D render suites that illustrate lighting temperature, surface textures, and spatial proportions.'),
      ('03', 'Materials & Finishes Schedule', 'Curated palettes of natural stone, wood veneers, plaster finishes, tiles, and bespoke coatings.'),
      ('04', 'Lighting & FF&E Schedules', 'Full technical specifications for architectural fixtures, decorative luminaires, and furniture pieces.'),
    ],
    steps=[
      ('Spatial Programming', 'Mapping client lifestyle, functional requirements, and spatial priorities.'),
      ('Concept & Material Moodboard', 'Establishing aesthetic mood, tonal palettes, and tactile sample curation.'),
      ('3D Visualisation & Detailing', 'Developing photo-real renders and refining joinery and ceiling details.'),
      ('Specifications & Procurement', 'Compiling comprehensive schedules for tender and artisan execution.'),
    ],
  ),
  'furniture': dict(
    h1='Bespoke Furniture & <em>Artisan Joinery</em>.',
    lede='Turning imagination and inspiration into custom furniture pieces that follow our architectural line, fit each space, and reflect client individuality.',
    overview_h='Pieces conceived for the exact geometry of the room.',
    p1='Standard manufactured furniture often compromises either the scale of a room or the distinctive identity of an architectural concept. At Nora AlSaud, we design custom standalone furniture, integrated joinery, and tailored cabinetry that speak the exact same aesthetic language as the building itself.',
    p2='Each piece is engineered with deep consideration for proportions, joinery craftsmanship, ergonomic comfort, and enduring materiality. We collaborate with master fabricators and carpenters to bring original pieces from preliminary sketch to finished installation.',
    badge='Custom Furniture Joinery & Specification',
    ref='NAS-FUR-01',
    deliv=[
      ('01', 'Custom Concept Designs', 'Original furniture pieces conceived specifically for the dimensions and character of the room.'),
      ('02', 'Joinery & Fabrication Drawings', 'Millwork construction drawings with sectional details, hardware specs, and tolerance thresholds.'),
      ('03', 'Material & Textile Curation', 'Handpicked hardwoods, architectural metals, premium leathers, and stain-resistant upholstery.'),
      ('04', 'Artisan Workshop Oversight', 'Collaboration with specialist workshops to verify sample mock-ups, joint strength, and finishing quality.'),
    ],
    steps=[
      ('Spatial & Ergonomic Brief', 'Measuring site alcoves, clearances, and defining the ergonomic brief for each piece.'),
      ('Design Drafting & Detailing', 'Drafting orthographic views, structural joints, and hardware integration.'),
      ('Material Sourcing & Mock-ups', 'Approving timber grain, marble veining, metal patina, and upholstery swatches.'),
      ('Fabrication Supervision', 'Overseeing workshop production, assembly trials, and final white-glove site delivery.'),
    ],
  ),
  'identity': dict(
    h1='Environmental Identity & <em>Brand Strategy</em>.',
    lede='Creating and developing logos, packaging, signage systems, and environmental branding that support commercial growth and sit naturally within architectural spaces.',
    overview_h='Visual identity rooted in three-dimensional space.',
    p1='Great commercial architecture and compelling visual identity are inseparable. When a brand’s spatial presence, signage, typography, and packaging reinforce one another, customers experience a cohesive narrative that builds lasting trust and emotional resonance.',
    p2='Our branding studio works at the intersection of graphic design and three-dimensional space. We formulate comprehensive brand identities—from core visual marks and typography systems to custom wayfinding, environmental graphics, and retail packaging—engineered for commercial longevity.',
    badge='Brand Geometry & Spatial Signage Layout',
    ref='NAS-IDE-01',
    deliv=[
      ('01', 'Brand Strategy & Positioning', 'Core brand narrative, tone of voice, values, and competitive market positioning.'),
      ('02', 'Logo System & Typography', 'Versatile primary, secondary, and sub-mark lockups with bespoke Arabic and Latin typography rules.'),
      ('03', 'Environmental Signage & Wayfinding', 'Spatial signage systems, entrance pylons, and directional graphics tailored to building finishes.'),
      ('04', 'Packaging & Collateral Suites', 'Product packaging, luxury shopping bags, menus, business stationery, and brand guidelines manual.'),
    ],
    steps=[
      ('Discovery & Strategic Foundation', 'Deep dive into business objectives, target audience demographics, and spatial context.'),
      ('Visual Exploration', 'Developing distinct design directions, typographic explorations, and conceptual marks.'),
      ('System Expansion', 'Extending the selected concept across spatial signage, digital collateral, and packaging mockups.'),
      ('Brand Guidelines & Handover', 'Delivering complete vector assets, color profiles, and comprehensive brand manual.'),
    ],
  ),
  'landscape': dict(
    h1='Landscape Architecture & <em>Outdoor Living</em>.',
    lede='Landscape and outdoor seating design that builds harmony between people and place, reinforcing the strong relationship between garden environments and architectural mass.',
    overview_h='Extending architecture into outdoor living sanctuaries.',
    p1='In the climate of the Arabian Gulf, outdoor spaces must be sculpted with intentionality. We treat the garden not as a decorative perimeter, but as an outdoor architectural room—an extension of interior living spaces that moderates microclimates, provides acoustic calm, and frames views.',
    p2='Our landscape design balances hardscape elements (paving, pergolas, retaining walls, swimming pools) with softscape selections tailored to regional heat and water efficiency. Every pathway, water feature, and lighting accent is carefully positioned to invite lingering.',
    badge='Landscape Master Plan & Hardscape Specification',
    ref='NAS-LAN-01',
    deliv=[
      ('01', 'Landscape Master Plan', 'Comprehensive site layout integrating courtyards, swimming pools, pathways, and entertaining terraces.'),
      ('02', 'Hardscape & Structural Features', 'Detailed plans for stone paving, custom pergolas, boundary walls, firepits, and water features.'),
      ('03', 'Climate-Adaptive Planting', 'Selection of drought-tolerant regional flora, shade trees, architectural cacti, and lush greenery.'),
      ('04', 'Irrigation & Atmospheric Lighting', 'Automated drip irrigation engineering and subtle low-glare nighttime illumination design.'),
    ],
    steps=[
      ('Microclimate & Soil Study', 'Assessing solar path, prevailing winds, soil conditions, and site privacy requirements.'),
      ('Outdoor Spatial Concept', 'Mapping outdoor zones: dining, lounging, water elements, and transitional green corridors.'),
      ('Hardscape & Planting Details', 'Selecting natural pavers, designing custom shade structures, and engineering plant layouts.'),
      ('Irrigation & Lighting Integration', 'Coordinating smart irrigation systems, drainage infrastructure, and landscape lighting circuits.'),
    ],
  ),
  'supervision': dict(
    h1='Project Supervision & <em>Site Execution</em>.',
    lede='Full monitoring and control of the project: analysing scope, available resources, and timing, with detailed reporting to protect quality and fidelity to the design.',
    overview_h='Guarding architectural fidelity from ground-break to handover.',
    p1='Even the most brilliant architectural vision can unravel if site execution lacks rigorous oversight. Our supervision team acts as the client’s dedicated technical guardian on site, ensuring that every detail on the drawings is translated into construction with uncompromised precision.',
    p2='We conduct structured site inspections, verify physical material mock-ups against approved specifications, monitor contractor milestones, and resolve unexpected site conditions proactively. Transparent reports keep clients fully informed without the burden of day-to-day site disputes.',
    badge='Site Supervision & Quality Audit Specification',
    ref='NAS-SUP-01',
    deliv=[
      ('01', 'Quality Control & Site Audits', 'Regular on-site inspections verifying structural integrity, material fidelity, and craftsmanship standards.'),
      ('02', 'Material Mock-up Approvals', 'Physical sample testing and sign-off on concrete, stone, timber, glazing, and MEP installations.'),
      ('03', 'Schedule & Resource Tracking', 'Continuous tracking of contractor milestones, progress timelines, and milestone verification.'),
      ('04', 'Client Reporting & Handover', 'Detailed photographic progress reports, snagging lists (punch lists), and final building handover audit.'),
    ],
    steps=[
      ('Pre-Construction Plan Review', 'Cross-referencing all architectural, structural, and MEP sets prior to ground-breaking.'),
      ('Milestone Site Inspections', 'Verifying key phases: foundations, concrete pours, waterproofing, rough-ins, and finishes.'),
      ('Quality & Material Verification', 'Testing on-site mock-ups, reviewing contractor submittals, and enforcing tolerances.'),
      ('Snagging & Project Handover', 'Documenting deficiency punch-lists, supervising rectification, and executing final handover.'),
    ],
  ),
 },
 'ar': {
  'architecture': dict(
    h1='التصميم المعماري و<em>التخطيط</em>.',
    lede='تصميم معماري متكامل للمشاريع السكنية والتجارية ومشاريع الاستخدام المختلط، نصيغه وفق أسلوب حياة العميل وتطلعاته ضمن خطنا المعماري المميّز.',
    overview_h='عمارة تستجيب للمكان والضوء وطبيعة الحياة.',
    p1='في نورة السعود معماريون ومهندسون، يمثّل التصميم المعماري نقطة التقاء الذكاء الفراغي بالمتانة الإنشائية والجمال الأصيل. نؤمن بأن العمارة يجب أن تستجيب لخصوصية المكان والمناخ في المملكة العربية السعودية، مع منح الفراغات مرونة وظيفية ووقاراً معمارياً يدوم عبر الزمن.',
    p2='من دراسات توجيه المبنى وتشكيل الكتل الأولى، وحتى استخراج رخص البناء والاعتمادات البلدية، يرافق مكتبنا في الخبر عملاءنا في كل خطوة. نحوّل المتطلبات المعقدة إلى كتل معمارية متناسقة تستفيد من الإضاءة الطبيعية وتوفر مساحات رحبة تعتمد على خامات أصيلة ومستدامة.',
    badge='مخطط معماري ونموذج تخطيطي',
    ref='NAS-ARC-01',
    deliv=[
      ('01', 'تشكيل الكتل ودراسات التوجيه', 'دراسة مسار الشمس والرياح ومسارات الحركة لضمان التوجيه الأمثل للكتلة المعمارية في الموقع.'),
      ('02', 'التصميم التخطيطي والنمذجة', 'مساقط أفقية وواجهات ونماذج ثلاثية الأبعاد تفصيلية توضح العلاقة بين الداخل والخارج.'),
      ('03', 'المخططات التنفيذية المتكاملة', 'إعداد مخططات البناء والتشطيبات والتنسيق الإنشائي والكهروميكانيكي (MEP) بدقة متناهية.'),
      ('04', 'التراخيص وكود البناء', 'مواءمة التصاميم بالكامل مع كود البناء السعودي (SBC) ومتابعة الاعتمادات البلدية والرسمية.'),
    ],
    steps=[
      ('دراسة الموقع والسياق', 'تحليل التضاريس والاشتراطات البلدية والزوايا البيئية المؤثرة على البناء.'),
      ('صياغة المفهوم والكتلة', 'تجسيد الأفكار في كتل معمارية أولية توازن بين الجمال والوظيفة.'),
      ('التطوير الهندسي والتفاصيل', 'دمج الأنظمة الهندسية واختيار الخامات المعمارية الخارجية والفتحات.'),
      ('المخططات التنفيذية والترخيص', 'إصدار حزمة المخططات التنفيذية وجداول الكميات ورخص البناء الرسمية.'),
    ],
  ),
  'interiors': dict(
    h1='التصميم الداخلي و<em>تنسيق الفراغات</em>.',
    lede='تصميم داخلي للفلل السكنية والشقق الفاخرة والمساحات التجارية، يجمع بين الانسيابية الوظيفية والأجواء الراقية.',
    overview_h='صياغة مساحات معيشية تنبض بالدفء والوقار.',
    p1='نتعامل مع التصميم الداخلي كتجربة معيشية متكاملة. نصيغ المساحة، والضوء، والتوازن الصوتي، والملمس الحسي للمواد لنخلق بيئات تمنح شعوراً بالراحة والرحابة والهدوء. كل تفصيلة في الفراغ مدروسة وفق حركة المستخدم وطريقة تفاعله مع المكان.',
    p2='من خلال دمج أعمال النجارة المخصصة، وسيناريوهات الإضاءة المتوازنة، والخامات الطبيعية النبيلة—كالرخام، وأخشاب الجوز، والبرونز المطفأ—نصنع مساحات تنبض بالأناقة دون تكلف. نرافق عملاءنا من المخططات التخطيطية وحتى لمسات التنسيق الأخيرة.',
    badge='منظور داخلي وتوزيع الإضاءة',
    ref='NAS-INT-01',
    deliv=[
      ('01', 'تخطيط المساحات وانسيابية الحركة', 'توزيع وظيفي متقن للمساحات يستثمر كل زاوية ويوفر حركة مريحة وإضاءة طبيعية.'),
      ('02', 'التصورات الواقعية ثلاثية الأبعاد', 'رندرات بصرية واقعية تبيّن درجات الإضاءة، وتفاصيل الخامات، وجماليات الفراغ.'),
      ('03', 'لوحات المواد والتشطيبات', 'خيارات مدروسة للرخام، والدهانات، والأرضيات، والتكسيات الجدارية المتناغمة.'),
      ('04', 'مخططات الإضاءة وجداول التأثيث', 'مواصفات تفصيلية لوحدات الإنارة المخفية والظاهرة، وقطع الأثاث، والإكسسوارات.'),
    ],
    steps=[
      ('البرمجة الفراغية', 'استيعاب نمط حياة العميل وتحديد الاحتياجات الوظيفية لكل فراغ.'),
      ('لوحة الأفكار والخامات', 'بناء المفهوم البصري وتنسيق عينات المواد والألوان والملامس.'),
      ('النمذجة والرندرة ثلاثية الأبعاد', 'إنتاج تصورات بصرية عالية الدقة مع تدقيق تفاصيل الأسقف والنجارة.'),
      ('جداول المواصفات والتنفيذ', 'إعداد المخططات التفصيلية وجداول الكميات والمواد للتنفيذ والشراء.'),
    ],
  ),
  'furniture': dict(
    h1='تصميم الأثاث المخصص و<em>أعمال النجارة</em>.',
    lede='تشكيل قطع أثاث تترجم فكرة التصميم بطريقة وظيفية تلائم المكان، وفق توجّهنا التصميمي واحتياج العميل.',
    overview_h='قطع مبتكرة خصيصاً لأبعاد وهندسة المكان.',
    p1='كثيراً ما يعجز الأثاث التجاري الجاهز عن تحقيق التوازن المثالي مع أبعاد الفراغ المعماري أو التعبير عن هوية التصميم. في نورة السعود، نبتكر قطع أثاث مستقلة وخزائن جدارية مخصصة تتناغم مع الروح المعمارية العامة للمكان وتتكامل معه كأنها جزء أصيل منه.',
    p2='تُصمم كل قطعة بعناية فائقة لنسب الأبعاد، والراحة الجسدية، ودقة التعاشيق الخشبية، وجودة الخامات المعمرة. نتعاون مع أمهر الحرفيين وورش النجارة المتخصصة لننقل القطعة من الرسم المبدئي إلى واقع ملموس في الفراغ.',
    badge='تفاصيل نجارة الأثاث والمواصفات الفنية',
    ref='NAS-FUR-01',
    deliv=[
      ('01', 'ابتكار تصاميم حصرية', 'قطع أثاث فريدة مصممة لتلائم تماماً أبعاد الفراغ المخصص لها وطبيعة استخدامه.'),
      ('02', 'رسومات النجارة التنفيذية', 'مخططات تفصيلية توضح زوايا التركيب، والإكسسوارات المخفية، وفواصل التمدد.'),
      ('03', 'اختيار الخامات والأقمشة', 'انتقاء أجود أنواع الأخشاب الطبيعية، والمعادن المصقولة، والجلود، والأقمشة المعمارية.'),
      ('04', 'الإشراف على التصنيع', 'مراجعة العينات الأولية في الورش والتأكد من دقة الصنعة والتشطيب النهائي قبل التوريد.'),
    ],
    steps=[
      ('القياس والدراسة الوظيفية', 'أخذ المقاسات الدقيقة في الموقع وتحديد المتطلبات المريحة للاستخدام.'),
      ('إعداد المخططات والرسومات', 'رسم المساقط والتفاصيل الإنشائية للقطعة وطرق تثبيتها.'),
      ('اعتماد العينات والخامات', 'مطابقة درجات الخشب، وعروق الرخام، وتدرجات المعادن، وعينات الأقمشة.'),
      ('متابعة الإنتاج والتركيب', 'الإشراف على التصنيع خطوة بخطوة حتى وصول القطعة وتركيبها بأعلى جودة.'),
    ],
  ),
  'identity': dict(
    h1='الهوية البصرية و<em>العلامة المكانية</em>.',
    lede='إنشاء وتطوير الشعار والعلامة التجارية وتصميم العبوات والمنتجات، بما يدعم نمو مشروع العميل ويتجانس مع تصميم المكان.',
    overview_h='هوية بصرية متجذرة في الفراغ ثلاثي الأبعاد.',
    p1='ترتبط العمارة التجارية الناجحة ارتباطاً وثيقاً بقوة الهوية البصرية. عندما تتكامل لوحات المحل والتصميم المكاني مع الشعار والخطوط والعبوات، يعيش العميل تجربة متصلة تعزز ثقته في المشروع وتترك أثراً دائماً في ذاكرته.',
    p2='يعمل فريق التصميم لدينا في المساحة الفاصلة بين التصميم الجرافيكي والفراغ المعماري ثلاثي الأبعاد. نبتكر هويات تجارية متكاملة—من الشعار والأنظمة الطباعية إلى أنظمة اللوحات الإرشادية وتغليف المنتجات—مصممة لدعم نجاح واستدامة الأعمال التجارية.',
    badge='هندسة الشعار وتطبيقات الهوية المكانية',
    ref='NAS-IDE-01',
    deliv=[
      ('01', 'استراتيجية وتموضع العلامة', 'صياغة رسالة العلامة، ونبرة الصوت، والقيم الجوهرية، وموقعها التنافسي في السوق.'),
      ('02', 'نظام الشعار والخطوط', 'تصميم الشعار بتطبيقاته المتعددة مع خطوط عربية ولاتينية متناغمة تعكس هوية المشروع.'),
      ('03', 'اللوحات الإرشادية والمكانية', 'تصميم أنظمة اللوحات والتوجيه المكاني المتوافقة مع تشطيبات وخامات المبنى.'),
      ('04', 'المطبوعات والتغليف', 'تصميم العبوات، والبطاقات، والقوائم، والأكياس، مع دليل إرشادي شامل للاستخدام.'),
    ],
    steps=[
      ('الاستكشاف والتأسيس الاستراتيجي', 'فهم أهداف العمل، والجمهور المستهدف، والعلاقة بين الفراغ والعلامة.'),
      ('التطوير البصري والمفاهيم', 'استكشاف أفكار الشعار، ودراسة الخطوط، وتناسق الألوان.'),
      ('التوسع في التطبيقات', 'تطبيق الهوية على اللوحات المكانية، والمطبوعات، ومواد التغليف والتواصل.'),
      ('دليل الهوية وتسليم الأصول', 'تسليم الملفات الرقمية بجميع الصيغ مع دليل المعايير القياسية للعلامة.'),
    ],
  ),
  'landscape': dict(
    h1='عمارة البيئة و<em>تصميم المساحات الخارجية</em>.',
    lede='تصميم الحدائق والجلسات الخارجية بما يبني الانسجام والتناغم بين المستخدم والمكان، مع التأكيد على العلاقة القوية بين تصميم الحدائق والتصميم المعماري.',
    overview_h='امتداد الفراغ المعماري إلى واحات معيشية خارجية.',
    p1='في مناخ الخليج العربي، تتطلب المساحات الخارجية تصميماً واعياً ومدروساً. نحن لا نتعامل مع الحديقة كمجرد مساحة محيطة بالمبنى، بل كفراغ معماري خارجي متكامل—امتداد حقيقي للمساحات الداخلية يخفف من وطأة الحرارة، ويوفر الهدوء والخصوصية، ويؤطر المشاهد البصرية الجميلة.',
    p2='يوازن تصميمنا بين العناصر الصلبة (الممرات، والمظلات، والجدران، والمسابح) والعناصر النباتية المختارة بعناية لتحمل المناخ وتوفير استهلاك المياه. يتم تحديد مواقع الجلسات والمسطحات المائية والإضاءة الليلية لتبني أجواء ساحرة تدعو للاسترخاء.',
    badge='المخطط العام للحدائق وتفاصيل العناصر الصلبة',
    ref='NAS-LAN-01',
    deliv=[
      ('01', 'المخطط العام للحدائق', 'توزيع متكامل للجلسات الخارجية، والمسابح، والممرات، ومناطق الضيافة المفتوحة.'),
      ('02', 'العناصر الإنشائية والصلبة', 'مخططات تفصيلية للأرضيات الحجرية، والمظلات الخشبية والمعدنية، والنوافير.'),
      ('03', 'الغطاء النباتي المتكيف', 'اختيار أشجار الظل والنباتات الإقليمية المتحملة للمناخ والموفرة للمياه.'),
      ('04', 'شبكات الري والإضاءة الليلية', 'تصميم شبكات الري بالتنقيط المؤتمتة وتوزيع الإنارة الخافتة الموجهة.'),
    ],
    steps=[
      ('دراسة المناخ والتربة', 'فحص مسار الشمس، والرياح السائدة، والتربة، ومستويات الخصوصية المطلوبة.'),
      ('المفهوم الفراغي الخارجي', 'توزيع مناطق الجلوس، والمسبح، والممرات الخضراء بما يتصل بالداخل.'),
      ('التفاصيل الإنشائية والنباتية', 'تحديد أنواع الحجر، وتفاصيل المظلات، وجداول أنواع النباتات وأماكن غرسها.'),
      ('شبكات البنية التحتية', 'تخطيط مسارات تصريف المياه، وشبكات الري الذكي، وتوصيلات الإضاءة.'),
    ],
  ),
  'supervision': dict(
    h1='الإشراف الهندسي و<em>إدارة التنفيذ</em>.',
    lede='إدارة ومراقبة المشروع بالكامل: تحليل نطاق العمل والموارد المتاحة والجدول الزمني، مع تقرير كامل ومفصل للعميل حرصاً على جودة التنفيذ ومطابقته للتصميم.',
    overview_h='حماية الهوية التصميمية من أول حفر في الموقع وحتى التسليم.',
    p1='مهما بلغت روعة الفكرة المعمارية ودقة المخططات، فإن غياب الإشراف الميداني الصارم قد يؤدي إلى نتائج لا تليق بالمشروع. يمثل فريق الإشراف لدينا عين العميل الهندسية الأمينة في الموقع، للتأكد من تنفيذ كل تفصيلة تصميمية بمطابقة تامة وأعلى مستويات الجودة.',
    p2='نقوم بجولات تفتيش دورية منتظمة، ونراجع عينات المواد ومطابقتها للمواصفات المعتمدة، ونراقب وتيرة الإنجاز وفق الجدول الزمني، ونتعامل مع التحديات الميدانية بحلول هندسية سريعة. نرفع لعملائنا تقارير دورية واضحة تجعلهم على دراية تامة بسير العمل دون عناء المتابعة اليومية.',
    badge='تقرير الإشراف الميداني وضبط الجودة',
    ref='NAS-SUP-01',
    deliv=[
      ('01', 'ضبط الجودة والمعاينات الميدانية', 'زيارات دورية لمراقبة دقة التنفيذ الإنشائي والمعماري ومطابقته للمخططات.'),
      ('02', 'مراجعة واعتماد عينات المواد', 'فحص العينات الواقعية للخرسانة، والرخام، والدهانات، والزجاج، والعزل قبل التركيب.'),
      ('03', 'متابعة الجداول الزمنية', 'مراقبة الالتزام بمواعيد الإنجاز المحددة والتحقق من الموارد والعمالة في الموقع.'),
      ('04', 'التقارير الشهرية والاستلام', 'إعداد تقارير دورية موثقة بالصور، وإدارة قائمة الملاحظات (Snagging)، والاستلام النهائي.'),
    ],
    steps=[
      ('مراجعة المخططات قبل البناء', 'مطابقة المخططات المعمارية والإنشائية والكهروميكانيكية لتلافي أي تعارض ميداني.'),
      ('التفتيش الميداني للمراحل الرئيسية', 'فحص القواعد، وصبات الخرسانة، وأعمال العزل، والتمديدات، والتشطيبات.'),
      ('مطابقة المواصفات والاختبارات', 'اختبار العينات الميدانية، ومراجعة اعتمادات المقاولين، وضبط دقة المقاسات.'),
      ('معالجة الملاحظات والاستلام', 'حصر الملاحظات النهائية، والإشراف على إنهائها، وتسليم المشروع جاهزاً للاستخدام.'),
    ],
  ),
 }
}

# (image key, category, EN caption, AR caption)
PROJECTS = [
 ('res-bedroom-1', 'residential', 'Bedroom — view 1', 'غرفة نوم — منظور 1'),
 ('com-cafe-8', 'commercial', 'Café — evening view', 'مقهى — منظر مسائي'),
 ('res-bath-1', 'residential', 'Bathroom — view 1', 'حمّام — منظور 1'),
 ('com-cafe-1', 'commercial', 'Café — layered timber counter', 'مقهى — الكاونتر الخشبي'),
 ('res-bedroom-2', 'residential', 'Bedroom — view 2', 'غرفة نوم — منظور 2'),
 ('com-cafe-5', 'commercial', 'Café — spiral staircase', 'مقهى — الدرج الحلزوني'),
 ('res-bedroom-3', 'residential', 'Bedroom — view 3', 'غرفة نوم — منظور 3'),
 ('com-cafe-4', 'commercial', 'Café — banquette seating', 'مقهى — جلسات الكنب'),
 ('res-dressing', 'residential', 'Dressing table', 'ركن التسريحة'),
 ('com-cafe-3', 'commercial', 'Café — feature wall', 'مقهى — الجدار المميز'),
 ('res-bath-2', 'residential', 'Bathroom — view 2', 'حمّام — منظور 2'),
 ('com-cafe-2', 'commercial', 'Café — counter and seating', 'مقهى — الكاونتر والجلسات'),
 ('res-bath-3', 'residential', 'Bathroom — view 3', 'حمّام — منظور 3'),
 ('com-cafe-6', 'commercial', 'Café — dining area', 'مقهى — منطقة الجلوس'),
 ('res-bath-4', 'residential', 'Bathroom — view 4', 'حمّام — منظور 4'),
 ('com-cafe-7', 'commercial', 'Café — upper level', 'مقهى — الطابق العلوي'),
 ('com-cafe-9', 'commercial', 'Café — counter view', 'مقهى — منظر الكاونتر'),
 ('com-cafe-10', 'commercial', 'Café — evening seating', 'مقهى — جلسات مسائية'),
]
HOME_WORK = ['res-bedroom-1', 'com-cafe-8', 'res-bath-1', 'com-cafe-1', 'res-bedroom-2', 'com-cafe-5']
OFFICE_ALT = {
 'en': {'office-sign': 'Reception area with the Nora AlSaud logo wall, two armchairs and a glass partition',
        'office-lounge': 'Open office with glass-partitioned meeting room and the Nora logo on the wall',
        'office-meeting': 'Meeting room with a glass table, black chairs and pendant lights',
        'office-open': 'Open-plan office floor seen through glass partitions',
        'office-glass': 'Glass-walled meeting room with pendant lights and black chairs'},
 'ar': {'office-sign': 'منطقة الاستقبال وجدار شعار نورة السعود مع كرسيين ومقسّم زجاجي',
        'office-lounge': 'مكتب مفتوح مع غرفة اجتماعات زجاجية وشعار نورة على الجدار',
        'office-meeting': 'غرفة اجتماعات بطاولة زجاجية وكراسٍ سوداء وإضاءة معلّقة',
        'office-open': 'مساحة العمل المفتوحة من خلف المقسمات الزجاجية',
        'office-glass': 'غرفة اجتماعات بجدران زجاجية وإضاءة معلّقة وكراسٍ سوداء'},
}
CAP_SUFFIX = {'en': 'design visualisation', 'ar': 'تصور تصميمي'}

# ---------------------------------------------------------------- helpers
def url(lang, key):
    return BASE + PATH[lang][key]

def img(name, alt, cls='', sizes='100vw', lazy=True, prio=False):
    m = MAN[name]; s = m['sizes']
    w = s[-1][1]; h = round(m['h'] * w / m['w'])
    srcset = f' srcset="{", ".join(f"/assets/img/{f} {sw}w" for f, sw in s)}" sizes="{sizes}"' if len(s) > 1 else ''
    load = 'fetchpriority="high"' if prio else ('loading="lazy"' if lazy else '')
    c = f' class="{cls}"' if cls else ''
    return f'<img src="/assets/img/{s[-1][0]}"{srcset} width="{w}" height="{h}" alt="{e(alt)}" decoding="async" {load}{c}>'

def full_src(name):
    return '/assets/img/' + MAN[name]['sizes'][-1][0]

def tel_html(disp=PHONE_DISP):
    return f'<bdi dir="ltr">{disp}</bdi>'

# ---------------------------------------------------------------- structured data
def ld_org(t):
    L = t['lang']
    return {
        '@type': 'ProfessionalService', '@id': f'{BASE}/#organization',
        'name': C['en']['name'], 'alternateName': [C['en']['alt_name'], C['ar']['name']],
        'url': f'{BASE}/', 'logo': {'@type': 'ImageObject', 'url': f'{BASE}/assets/img/icon-512.png', 'width': 512, 'height': 512},
        'image': f'{BASE}/assets/img/og-share.jpg', 'email': EMAIL, 'telephone': PHONE_TEL,
        'description': C['en']['meta']['home'][1],
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Prince Turki Street, Jarir Plaza, Second Floor, Office 203', 'addressLocality': 'Khobar', 'addressCountry': 'SA'},
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '08:00', 'closes': '17:00'}],
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': PHONE_TEL, 'email': EMAIL, 'availableLanguage': ['English', 'Arabic']}],
        'knowsAbout': [SERV['en'][s][0] for s in SERV_SLUGS],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': SERV['en'][s][0], 'url': f'{BASE}/services/{s}/'}} for s in SERV_SLUGS],
    }

def ld_graph(lang, key, extra=None):
    t = C[lang]; title, desc = t['meta'][key]; u = url(lang, key)
    ptype = {'about': 'AboutPage', 'contact': 'ContactPage', 'projects': 'CollectionPage'}.get(key, 'WebPage')
    graph = [
        ld_org(t),
        {'@type': 'WebSite', '@id': f'{BASE}/#website', 'url': f'{BASE}/', 'name': C['en']['name'], 'inLanguage': ['en', 'ar'], 'publisher': {'@id': f'{BASE}/#organization'}},
        {'@type': ptype, '@id': u + '#webpage', 'url': u, 'name': title, 'description': desc, 'inLanguage': lang,
         'isPartOf': {'@id': f'{BASE}/#website'}, 'about': {'@id': f'{BASE}/#organization'},
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': f'{BASE}/assets/img/og-share.jpg'}},
    ]
    if key != 'home':
        if key.startswith('service_'):
            slug = key.replace('service_', '')
            svc_name = SERV[lang][slug][0]
            graph.append({'@type': 'BreadcrumbList', '@id': u + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': t['nav']['home'], 'item': url(lang, 'home')},
                {'@type': 'ListItem', 'position': 2, 'name': t['nav']['services'], 'item': url(lang, 'services')},
                {'@type': 'ListItem', 'position': 3, 'name': svc_name, 'item': u}]})
        else:
            graph.append({'@type': 'BreadcrumbList', '@id': u + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': t['nav']['home'], 'item': url(lang, 'home')},
                {'@type': 'ListItem', 'position': 2, 'name': t['nav'][key], 'item': u}]})
        graph[2]['breadcrumb'] = {'@id': u + '#breadcrumb'}
    if extra:
        graph.extend(extra)
    return {'@context': 'https://schema.org', '@graph': graph}

# ---------------------------------------------------------------- shell
HEAD_SCRIPT = ("(function(){var r=document.documentElement,t;try{t=localStorage.getItem('nora-theme')}catch(e){}"
               "if(t!=='light'&&t!=='dark'){t='light'}"
               "r.dataset.theme=t;r.classList.add('js');var m=document.querySelector('meta[name=theme-color]');"
               "if(m)m.content=t==='dark'?'#0a0c0e':'#e9e5dc'})()")

def shell(lang, key, main, extra_ld=None, noindex=False, canonical=None, title=None, desc=None):
    t = C[lang]; o = t['other']
    title = title or t['meta'][key][0]; desc = desc or t['meta'][key][1]
    can = canonical or url(lang, key)
    ui = t['ui']
    fonts = ('<link rel="preload" href="/assets/fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>') if lang == 'en' else (
             '<link rel="preload" href="/assets/fonts/ibm-plex-sans-arabic-arabic-300-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="/assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2" as="font" type="font/woff2" crossorigin>')
    alts = ''
    if not noindex:
        alts = (f'<link rel="alternate" hreflang="ar" href="{url("ar", key)}">\n<link rel="alternate" hreflang="en" href="{url("en", key)}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{url("ar", key)}">')
    ld = ''
    if not noindex:
        ld = f'<script type="application/ld+json">{json.dumps(ld_graph(lang, key, extra_ld), ensure_ascii=False, separators=(",", ":"))}</script>'
    og_img = f'{BASE}/assets/img/og-share.jpg'
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    nav_list = []
    mnav_list = []
    is_services = (key == 'services' or key.startswith('service_'))
    for k in PAGES:
        if k == 'services':
            svc_cur = ' aria-current="page"' if is_services else ''
            all_cur = ' aria-current="page"' if key == 'services' else ''
            dd_sub = ''.join(
                f'<li><a href="{PATH[lang]["service_" + s]}"{" aria-current=\"page\"" if key == "service_" + s else ""}><span>0{i}</span>{e(SERV[lang][s][0])}</a></li>'
                for i, s in enumerate(SERV_SLUGS, 1)
            )
            nav_list.append(
                f'<div class="nav-dd">'
                f'<a href="{PATH[lang]["services"]}" class="nav-dd-link"{svc_cur}>'
                f'{e(t["nav"]["services"])}'
                f'<svg class="dd-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
                f'</a>'
                f'<ul class="nav-dd-menu glass">'
                f'<li><a href="{PATH[lang]["services"]}"{all_cur}><strong>{e(t["ui"]["all_services"])}</strong></a></li>'
                f'{dd_sub}'
                f'</ul>'
                f'</div>'
            )
            msub = ''.join(
                f'<a href="{PATH[lang]["service_" + s]}"{" aria-current=\"page\"" if key == "service_" + s else ""}>{e(SERV[lang][s][0])}</a>'
                for s in SERV_SLUGS
            )
            mnav_list.append(
                f'<div class="mnav-svc">'
                f'<a href="{PATH[lang]["services"]}"{svc_cur}>{e(t["nav"]["services"])}</a>'
                f'<div class="mnav-sub">{msub}</div>'
                f'</div>'
            )
        else:
            cur = ' aria-current="page"' if k == key else ''
            nav_list.append(f'<a href="{PATH[lang][k]}"{cur}>{e(t["nav"][k])}</a>')
            mnav_list.append(f'<a href="{PATH[lang][k]}"{cur}>{e(t["nav"][k])}</a>')
    nav_items = ''.join(nav_list)
    mnav_items = ''.join(mnav_list)
    og_alt = (CAP_SUFFIX[lang].capitalize() if lang == 'en' else CAP_SUFFIX[lang]) + ': ' + t['hero']['cap_v'].split(' · ')[0]
    other_href = PATH[o].get(key, PATH[o]['home'])
    head = f'''<!doctype html>
<html lang="{lang}" dir="{t['dir']}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#e9e5dc">
<script>{HEAD_SCRIPT}</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{can}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(t['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{C[o]['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{fonts}
<link rel="stylesheet" href="/assets/css/main.css">
{ld}
</head>'''
    header = f'''<body>
<a class="skip" href="#main">{e(ui['skip'])}</a>
<div class="ambient" aria-hidden="true"></div><div class="gridlines" aria-hidden="true"></div>
<header class="hdr glass">
  <a class="brand" href="{PATH[lang]['home']}" aria-label="{e(t['name'])}">
    <span class="brand-mark"><img src="/assets/img/mark.webp" alt="" width="{MAN['mark']['w']}" height="{MAN['mark']['h']}"></span>
    <span class="brand-txt"><span class="brand-name">{e(t['short'])}</span><span class="brand-sub">{e(t['sub'])}</span></span>
  </a>
  <nav class="nav" aria-label="{e(ui['primary_nav'])}">{nav_items}</nav>
  <div class="hdr-ctl">
    <a class="lang-sw" href="{other_href}" hreflang="{o}" lang="{o}" aria-label="{e(t['switch_label'])}">{e(t['switch'])}</a>
    <button class="theme-toggle" type="button" role="switch" aria-checked="false" aria-label="{e(ui['theme'])}">{SUN}{MOON}<span class="thumb"></span></button>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="{e(ui['menu'])}"><span></span></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="{e(ui['mobile_nav'])}">{mnav_items}</nav>
<main id="main" tabindex="-1">
'''
    f = t['footer']
    footer_links = ''.join(f'<li><a href="{PATH[lang][k]}">{e(t["nav"][k])}</a></li>' for k in PAGES)
    footer = f'''
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div class="ftr-brand">
        <a class="brand" href="{PATH[lang]['home']}"><span class="brand-mark"><img src="/assets/img/mark.webp" alt="" width="{MAN['mark']['w']}" height="{MAN['mark']['h']}" loading="lazy"></span><span class="brand-txt"><span class="brand-name">{e(t['short'])}</span><span class="brand-sub">{e(t['sub'])}</span></span></a>
        <p>{e(f['blurb'])}</p>
      </div>
      <div><h2>{e(f['explore'])}</h2><ul>{footer_links}</ul></div>
      <div><h2>{e(f['visit'])}</h2>
        <address>{e(t['address'])}<br><a href="{MAPS}" rel="noopener" target="_blank">{e(ui['open_maps'])}</a></address>
        <ul style="margin-block-start:1rem"><li><a href="tel:{PHONE_TEL}">{tel_html()}</a></li><li><a href="mailto:{EMAIL}"><bdi dir="ltr">{EMAIL}</bdi></a></li></ul></div>
      <div><h2>{e(f['hours'])}</h2><p>{e(t['days'])}<br>{e(t['hours'])}</p></div>
    </div>
    <div class="ftr-bar"><span>© {YEAR} {e(t['name'])}. {e(f['rights'])}</span><a href="{other_href}" hreflang="{o}" lang="{o}">{e(t['switch'])}</a></div>
  </div>
</footer>
<button class="btt glass" type="button" aria-label="{e(ui['btt'])}">
  <svg class="ring" viewBox="0 0 36 36" aria-hidden="true"><circle class="tr" cx="18" cy="18" r="16" pathLength="100"/><circle class="pg" cx="18" cy="18" r="16" pathLength="100"/></svg>
  {UP}
</button>
<script type="application/json" id="i18n">{json.dumps(t['i18n'], ensure_ascii=False)}</script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    return head + header + main + footer

def phero(lang, key, eyebrow, h1, lede=''):
    t = C[lang]
    return f'''<section class="phero"><div class="wrap">
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="{PATH[lang]['home']}">{e(t['ui']['home'])}</a></li><li aria-current="page">{e(t['nav'][key])}</li></ol>
  <span class="eyebrow">{e(eyebrow)}</span>
  <h1 class="h-xl">{h1}</h1>
  {f'<p class="lede">{e(lede)}</p>' if lede else ''}
</div></section>'''

def sec_head(eyebrow, h, lede):
    return f'''<div class="sec-head"><div class="rv"><span class="eyebrow">{e(eyebrow)}</span><h2 class="h-lg" style="margin-block-start:1rem">{h}</h2></div><p class="lede rv" style="--d:.1s">{e(lede)}</p></div>'''

def svc_rows(lang):
    out = []
    for i, s in enumerate(SERV_SLUGS, 1):
        n, d = SERV[lang][s]
        out.append(f'<a class="svc rv" href="{PATH[lang][f"service_{s}"]}" style="--d:{i*.04:.2f}s"><span class="svc-n">0{i}</span><h3 class="svc-t">{e(n)}</h3><p class="svc-d">{e(d)}</p>{ARROW}</a>')
    return f'<div class="svc-list">{"".join(out)}</div>'

def steps_html(lang):
    out = ''.join(f'<li class="step rv" style="--d:{i*.05:.2f}s"><span class="step-n">0{i}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(STEPS[lang], 1))
    return f'<ol class="steps">{out}</ol>'

def film_html(lang):
    t = C[lang]; f = t['film']
    return f'''<section class="section"><div class="wrap"><div class="film">
  <div class="film-frame glass rv">
    {img('office-open', OFFICE_ALT[lang]['office-open'], 'poster', '(min-width:960px) 58vw, 100vw')}
    <video preload="none" playsinline aria-label="{e(f['h'])}"><source src="/assets/video/noras-office.mp4" type="video/mp4"></video>
    <button class="play glass" type="button" aria-label="{e(t['ui']['play'])}">{PLAY}</button>
  </div>
  <div class="film-copy rv" style="--d:.1s"><span class="eyebrow">{e(f['eyebrow'])}</span><h2 class="h-lg" style="margin-block:1rem">{e(f['h'])}</h2><p class="lede">{e(f['p'])}</p></div>
</div></div></section>'''

def cta_html(lang):
    t = C[lang]; c = t['cta']
    return f'''<section class="section" style="padding-block-start:0"><div class="wrap"><div class="cta glass rv">
  <span class="eyebrow">{e(t['nav']['contact'])}</span>
  <h2 class="h-lg" style="margin-block-start:1rem">{c['h']}</h2>
  <p class="lede" style="margin-block-start:1rem">{e(c['p'])}</p>
  <div class="cta-row"><a class="btn btn-solid" href="{PATH[lang]['contact']}">{e(c['a'])}{ARROW}</a><a class="btn btn-ghost" href="{PATH[lang]['careers']}">{e(c['b'])}</a></div>
</div></div></section>'''

# ---------------------------------------------------------------- pages
def page_home(lang):
    t = C[lang]; h = t['hero']; i = t['intro']; ui = t['ui']
    facts = ''.join(f'<div class="fact"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in t['facts'])
    cap = CAP_SUFFIX[lang]
    works = []
    works_dup = []
    cap_idx = {p[0]: p for p in PROJECTS}
    for k in HOME_WORK:
        _, cat, en_c, ar_c = cap_idx[k]
        c = en_c if lang == 'en' else ar_c
        works.append(f'<article class="work"><a href="{PATH[lang]["projects"]}#{cat}" aria-label="{e(c)}">{img(k, c + " — " + cap, "", "(min-width:700px) 600px, 72vw")}<span class="work-cap glass"><span>{e(c)}</span><small>{e(ui[cat])}</small></span></a></article>')
        works_dup.append(f'<article class="work" aria-hidden="true"><a href="{PATH[lang]["projects"]}#{cat}" tabindex="-1" aria-hidden="true">{img(k, c + " — " + cap, "", "(min-width:700px) 600px, 72vw")}<span class="work-cap glass"><span>{e(c)}</span><small>{e(ui[cat])}</small></span></a></article>')
    hero_alt = f"{t['hero']['cap_v'].split(' · ')[0]} — {cap}"
    hero_img = img('res-bedroom-1', hero_alt, '', '(min-width:960px) 40vw, 90vw', lazy=False, prio=True).replace('<img ', '<img data-parallax ')
    main = f'''<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow rv">{e(h['eyebrow'])}</span>
    <h1 class="h-xl rv" style="--d:.08s">{h['h1']}</h1>
    <p class="lede rv" style="--d:.16s">{e(h['lede'])}</p>
    <div class="hero-cta rv" style="--d:.24s"><a class="btn btn-solid" href="{PATH[lang]['projects']}">{e(ui['view_projects'])}{ARROW}</a><a class="btn btn-ghost" href="{PATH[lang]['services']}">{e(ui['our_services'])}</a></div>
  </div>
  <div class="arch rv" style="--d:.2s">
    <div class="arch-frame">{hero_img}</div>
    <div class="arch-cap glass"><b>{e(h['cap_k'])}</b>{e(h['cap_v'])}</div>
  </div>
</div></section>
<div class="facts"><div class="wrap"><div class="facts-bar glass rv">{facts}</div></div></div>

<section class="section"><div class="wrap intro">
  <div class="intro-main rv"><span class="eyebrow">{e(i['eyebrow'])}</span><p class="intro-stmt" style="margin-block-start:1.4rem">{i['stmt']}</p><p class="lede">{e(i['p'])}</p></div>
  <aside class="vision glass rv" style="--d:.12s"><span class="eyebrow">{e(i['vision_k'])}</span><p>{e(i['vision'])}</p></aside>
</div></section>

<section class="section" style="padding-block-start:0"><div class="wrap">
  {sec_head(t['svc']['eyebrow'], t['svc']['h'], t['svc']['lede'])}
  {svc_rows(lang)}
</div></section>

<section class="section" style="padding-inline:0"><div class="wrap">
  <div class="sec-head"><div class="rv"><span class="eyebrow">{e(t['work']['eyebrow'])}</span><h2 class="h-lg" style="margin-block-start:1rem">{e(t['work']['h'])}</h2>{f'<p class="lede" style="margin-block-start:1rem">{e(t["work"]["lede"])}</p>' if t['work'].get('lede') else ''}</div>
  <div class="rv" style="--d:.1s">
    <div class="rail-ctl"><button class="rbtn prev glass" type="button" aria-label="{e(ui['rail_prev'])}">{CHEV}</button><button class="rbtn next glass" type="button" aria-label="{e(ui['rail_next'])}">{CHEV}</button><a class="link-arrow" style="margin-inline-start:1rem" href="{PATH[lang]['projects']}">{e(ui['all_projects'])}{ARROW}</a></div></div></div>
</div>
<div class="rail-wrap"><div class="rail" role="region" aria-label="{e(ui['gallery'])}" tabindex="0"><div class="rail-track"><div class="rail-group">{"".join(works)}</div><div class="rail-group" aria-hidden="true">{"".join(works_dup)}</div><div class="rail-group" aria-hidden="true">{"".join(works_dup)}</div></div></div></div>
</section>

<section class="section" style="padding-block-start:0"><div class="wrap">
  <div class="sec-head"><div class="rv"><span class="eyebrow">{e(t['process']['eyebrow'])}</span><h2 class="h-lg" style="margin-block-start:1rem">{e(t['process']['h'])}</h2></div></div>
  {steps_html(lang)}
</div></section>
{film_html(lang)}
{cta_html(lang)}
'''
    return shell(lang, 'home', main)

ABOUT = {
 'en': dict(eyebrow='About us', h1='Who we <em>are</em>.', lede='Nora AlSaud Architects & Engineers is an engineering office with considerable experience and a lot of passion.',
            p1='We provide engineering and design services at a high level of professionalism and reliability. Our professional experience is our main guide.',
            p2='We listen to our clients’ vision and concepts and transform them into area, space and mass.',
            vk='Our vision', v='Create a renewed, creative <em>architectural environment</em> that reflects on society and affects it positively.',
            gallery='The office', story_alt='office-sign'),
 'ar': dict(eyebrow='من نحن', h1='من <em>نحن</em>؟', lede='نورة السعود معماريون ومهندسون: مكتب هندسي بخبرة مهنية وشغف كبير.',
            p1='نقدّم الخدمات الهندسية والتصميمية على مستوى عالٍ من الاحترافية والدقة، والخبرة المهنية الثرية هي الموجّه الأساسي لنا.',
            p2='نستمع لعملائنا ونقرأ تطلعاتهم لإخراجها في المساحة والفراغ والكتلة.',
            vk='رؤيتنا', v='تشكيل <em>بيئة عمرانية</em> إبداعية متجددة تنعكس بدورها على المجتمع وتؤثر فيه إيجاباً.',
            gallery='المكتب', story_alt='office-sign'),
}

def page_about(lang):
    t = C[lang]; a = ABOUT[lang]; ui = t['ui']
    mos = ''.join(f'<figure class="rv" style="--d:{i*.06:.2f}s">{img(k, OFFICE_ALT[lang][k], "", "(min-width:960px) 67vw, (min-width:640px) 50vw, 100vw")}</figure>' for i, k in enumerate(['office-lounge', 'office-meeting', 'office-glass', 'office-open']))
    main = f'''{phero(lang, 'about', a['eyebrow'], a['h1'], a['lede'])}
<section class="section" style="padding-block-start:1rem"><div class="wrap story">
  <div class="story-img glass rv">{img('office-sign', OFFICE_ALT[lang]['office-sign'], '', '(min-width:960px) 50vw, 100vw', lazy=False)}</div>
  <div class="story-body rv" style="--d:.1s"><p>{e(a['p1'])}</p><p>{e(a['p2'])}</p><p style="margin-block-start:2rem"><a class="link-arrow" href="{PATH[lang]['services']}">{e(ui['our_services'])}{ARROW}</a></p></div>
</div></section>
<section class="section" style="padding-block-start:0;padding-block-end:clamp(1.5rem,3.5vw,2.5rem)"><div class="wrap"><div class="vision-block glass rv"><span class="eyebrow">{e(a['vk'])}</span><p class="pull">{a['v']}</p></div></div></section>
<section class="section" style="padding-block-start:0"><div class="wrap">
  <div class="sec-head"><div class="rv"><span class="eyebrow">{e(a['gallery'])}</span></div></div>
  <div class="mosaic">{mos}</div>
</div></section>
{film_html(lang)}
{cta_html(lang)}
'''
    return shell(lang, 'about', main)

SVC_PAGE = {
 'en': dict(eyebrow='Services', h1='Design and delivery, <em>one office</em>.', lede='Six disciplines that work together, from the first concept to supervision on site.'),
 'ar': dict(eyebrow='خدماتنا', h1='تصميم وتنفيذ، <em>مكتب واحد</em>.', lede='ست خدمات تعمل معاً، من الفكرة الأولى إلى الإشراف في الموقع.'),
}

def page_services(lang):
    t = C[lang]; s = SVC_PAGE[lang]; ui = t['ui']
    nav = ''.join(f'<li><a href="#{k}"><span>0{i}</span>{e(SERV[lang][k][0])}</a></li>' for i, k in enumerate(SERV_SLUGS, 1))
    blocks = ''.join(
        f'<section class="svc-block rv" id="{k}"><span class="num">0{i}</span><h2 class="h-lg"><a href="{PATH[lang][f"service_{k}"]}">{e(SERV[lang][k][0])}</a></h2><p>{e(SERV[lang][k][1])}</p>'
        f'<div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-block-start:1.4rem">'
        f'<a class="link-arrow" href="{PATH[lang][f"service_{k}"]}">{e(ui["view_service"])}{ARROW}</a>'
        + (f'<a class="link-arrow" href="{PATH[lang]["projects"]}">{e(ui["related"])}{ARROW}</a>' if k in ('architecture', 'interiors', 'furniture') else '')
        + '</div></section>'
        for i, k in enumerate(SERV_SLUGS, 1))
    ld = [{'@type': 'ItemList', '@id': url(lang, 'services') + '#services', 'name': t['meta']['services'][0],
           'itemListElement': [{'@type': 'ListItem', 'position': i, 'item': {'@type': 'Service', 'name': SERV[lang][k][0], 'description': SERV[lang][k][1], 'url': url(lang, f'service_{k}'), 'provider': {'@id': f'{BASE}/#organization'}}} for i, k in enumerate(SERV_SLUGS, 1)]}]
    main = f'''{phero(lang, 'services', s['eyebrow'], s['h1'], s['lede'])}
<section class="section" style="padding-block-start:1rem"><div class="wrap svc-page">
  <nav class="svc-nav" aria-label="{e(t['nav']['services'])}"><ul class="glass">{nav}</ul></nav>
  <div class="svc-blocks">{blocks}</div>
</div></section>
<section class="section" style="padding-block-start:0"><div class="wrap">
  <div class="sec-head"><div class="rv"><span class="eyebrow">{e(t['process']['eyebrow'])}</span><h2 class="h-lg" style="margin-block-start:1rem">{e(t['process']['h'])}</h2></div></div>
  {steps_html(lang)}
</div></section>
{cta_html(lang)}
'''
    return shell(lang, 'services', main, ld)

def blueprint_svg(slug, lang):
    grid = (
        '<defs>'
        '<pattern id="bp-grid-fine" width="20" height="20" patternUnits="userSpaceOnUse">'
        '<path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.09"/>'
        '</pattern>'
        '<pattern id="bp-grid-major" width="100" height="100" patternUnits="userSpaceOnUse">'
        '<rect width="100" height="100" fill="url(#bp-grid-fine)"/>'
        '<path d="M 100 0 L 0 0 0 100" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.18"/>'
        '</pattern>'
        '</defs>'
        '<rect width="800" height="500" fill="url(#bp-grid-major)"/>'
        '<path d="M 25 35 L 25 25 L 35 25 M 765 25 L 775 25 L 775 35 M 25 465 L 25 475 L 35 475 M 765 475 L 775 475 L 775 465" stroke="var(--ink-3)" stroke-width="1.2" fill="none"/>'
    )
    
    if slug == 'architecture':
        shapes = (
            '<!-- Ground Isometric Grid -->'
            '<path d="M 120 400 L 400 480 L 680 400 L 400 320 Z" stroke="currentColor" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
            '<path d="M 190 380 L 400 440 L 610 380 L 400 320 Z" stroke="currentColor" stroke-opacity="0.15" stroke-width="0.8" fill="none"/>'
            '<!-- Villa Massing -->'
            '<path d="M 220 370 L 400 425 L 580 370 L 580 320 L 400 375 L 220 320 Z" stroke="currentColor" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.6"/>'
            '<path d="M 260 320 L 400 365 L 400 190 L 260 145 Z" stroke="currentColor" stroke-width="1.6" fill="var(--surface)" fill-opacity="0.8"/>'
            '<path d="M 400 365 L 540 320 L 540 145 L 400 190 Z" stroke="currentColor" stroke-width="1.6" fill="var(--surface)" fill-opacity="0.9"/>'
            '<!-- Cantilevered Upper Roof -->'
            '<path d="M 400 170 L 230 120 L 370 75 L 540 125 Z" stroke="var(--accent)" stroke-width="2" fill="var(--surface)" fill-opacity="0.7"/>'
            '<path d="M 400 180 L 230 130 L 230 120 L 400 170 L 540 125 L 540 135 Z" stroke="var(--accent)" stroke-width="1.5" fill="var(--accent)" fill-opacity="0.2"/>'
            '<!-- Vertical Louvers -->'
            '<path d="M 290 305 L 290 165 M 320 315 L 320 175 M 350 325 L 350 185 M 380 335 L 380 195" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6"/>'
            '<path d="M 430 350 L 430 205 M 460 340 L 460 195 M 490 330 L 490 185 M 520 320 L 520 175" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6"/>'
            '<!-- Dimensions & Datums -->'
            '<line x1="200" y1="120" x2="200" y2="400" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="3 3"/>'
            '<path d="M 195 120 L 205 120 M 195 400 L 205 400" stroke="var(--ink-3)" stroke-width="1.2"/>'
            '<text x="185" y="265" font-family="monospace" font-size="11" fill="var(--ink-2)" text-anchor="end">+10.20m</text>'
            '<!-- North Arrow -->'
            '<g transform="translate(710, 70)">'
            '<circle cx="0" cy="0" r="22" stroke="currentColor" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
            '<path d="M 0 -18 L 6 12 L 0 6 L -6 12 Z" fill="var(--accent)"/>'
            '<text x="0" y="-23" font-family="monospace" font-size="10" font-weight="bold" fill="var(--accent-text)" text-anchor="middle">N</text>'
            '</g>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">ELEVATION A-A · SCHEMATIC MASSING · SCALE 1:100</text>'
        )
    elif slug == 'interiors':
        shapes = (
            '<!-- Vanishing point perspective lines -->'
            '<line x1="400" y1="230" x2="60" y2="40" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
            '<line x1="400" y1="230" x2="740" y2="40" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
            '<line x1="400" y1="230" x2="60" y2="460" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
            '<line x1="400" y1="230" x2="740" y2="460" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
            '<!-- Back Wall -->'
            '<rect x="250" y="130" width="300" height="210" stroke="currentColor" stroke-width="1.5" fill="var(--surface)" fill-opacity="0.6"/>'
            '<!-- Coffered Ceiling Grid -->'
            '<path d="M 250 130 L 120 70 M 350 130 L 290 60 M 450 130 L 510 60 M 550 130 L 680 70" stroke="currentColor" stroke-opacity="0.35" stroke-width="1"/>'
            '<path d="M 180 100 L 620 100" stroke="var(--accent)" stroke-opacity="0.6" stroke-width="1.2" stroke-dasharray="6 3"/>'
            '<!-- Recessed Feature Wall Panelling -->'
            '<rect x="280" y="150" width="110" height="170" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2" fill="none"/>'
            '<rect x="410" y="150" width="110" height="170" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2" fill="none"/>'
            '<!-- Minimalist Sofa & Table in Perspective -->'
            '<path d="M 280 320 L 520 320 L 550 375 L 250 375 Z" stroke="var(--accent)" stroke-width="1.8" fill="var(--surface)" fill-opacity="0.9"/>'
            '<path d="M 280 290 L 520 290 L 520 320 L 280 320 Z" stroke="currentColor" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.7"/>'
            '<path d="M 330 385 L 470 385 L 485 415 L 315 415 Z" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/>'
            '<!-- Floor Tile Grid -->'
            '<line x1="400" y1="230" x2="280" y2="460" stroke="currentColor" stroke-opacity="0.2" stroke-width="0.8"/>'
            '<line x1="400" y1="230" x2="520" y2="460" stroke="currentColor" stroke-opacity="0.2" stroke-width="0.8"/>'
            '<line x1="170" y1="410" x2="630" y2="410" stroke="currentColor" stroke-opacity="0.2" stroke-width="0.8"/>'
            '<!-- Pendant Light Fixture -->'
            '<line x1="400" y1="90" x2="400" y2="165" stroke="currentColor" stroke-width="1"/>'
            '<path d="M 380 175 L 420 175 L 410 165 L 390 165 Z" fill="var(--accent)"/>'
            '<circle cx="400" cy="180" r="3" fill="var(--accent)"/>'
            '<path d="M 360 230 L 400 180 L 440 230" stroke="var(--accent)" stroke-opacity="0.35" stroke-dasharray="3 3" fill="none"/>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">SECTION B-B · INTERIOR VOLUME &amp; ILLUMINATION DRAFT</text>'
        )
    elif slug == 'furniture':
        shapes = (
            '<!-- Orthographic Framing Grid -->'
            '<rect x="180" y="90" width="440" height="340" stroke="currentColor" stroke-opacity="0.2" stroke-width="0.8" stroke-dasharray="4 4" fill="none"/>'
            '<!-- Bespoke Armchair Axonometric Drafting -->'
            '<path d="M 320 330 L 480 330 L 510 270 L 350 270 Z" stroke="var(--accent)" stroke-width="1.8" fill="var(--surface)" fill-opacity="0.8"/>'
            '<path d="M 320 330 L 320 220 L 350 160 L 350 270 Z" stroke="currentColor" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.6"/>'
            '<path d="M 350 160 L 510 160 L 510 270 L 350 270 Z" stroke="currentColor" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.7"/>'
            '<!-- Chair Legs & Wood Joinery Details -->'
            '<line x1="325" y1="330" x2="320" y2="390" stroke="currentColor" stroke-width="2.2"/>'
            '<line x1="475" y1="330" x2="480" y2="390" stroke="currentColor" stroke-width="2.2"/>'
            '<line x1="505" y1="270" x2="515" y2="330" stroke="currentColor" stroke-width="2.2"/>'
            '<line x1="355" y1="270" x2="350" y2="330" stroke="currentColor" stroke-width="2.2"/>'
            '<!-- Dimension Callouts -->'
            '<line x1="300" y1="160" x2="300" y2="390" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="2 2"/>'
            '<path d="M 295 160 L 305 160 M 295 390 L 305 390" stroke="var(--ink-3)" stroke-width="1"/>'
            '<text x="285" y="280" font-family="monospace" font-size="10" fill="var(--ink-2)" text-anchor="end">H: 740 mm</text>'
            '<line x1="320" y1="410" x2="480" y2="410" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="2 2"/>'
            '<text x="400" y="425" font-family="monospace" font-size="10" fill="var(--ink-2)" text-anchor="middle">W: 820 mm</text>'
            '<!-- Joinery Inset Magnifier -->'
            '<g transform="translate(630, 160)">'
            '<circle cx="0" cy="0" r="45" stroke="var(--accent)" stroke-width="1.5" fill="var(--surface)" fill-opacity="0.9"/>'
            '<path d="M -20 -15 L 20 -15 L 10 15 L -10 15 Z" stroke="currentColor" stroke-width="1.2" fill="none"/>'
            '<line x1="0" y1="-25" x2="0" y2="25" stroke="var(--accent)" stroke-width="1" stroke-dasharray="2 2"/>'
            '<text x="0" y="32" font-family="monospace" font-size="9" fill="var(--accent-text)" text-anchor="middle">MORTISE &amp; TENON</text>'
            '</g>'
            '<path d="M 505 200 L 585 170" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 3"/>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">ORTHOGRAPHIC PROJECTION · CUSTOM JOINERY SPECIFICATION</text>'
        )
    elif slug == 'identity':
        shapes = (
            '<!-- Geometric Circle Construction Grid -->'
            '<g transform="translate(370, 220)">'
            '<circle cx="0" cy="0" r="140" stroke="currentColor" stroke-opacity="0.15" stroke-width="1" fill="none"/>'
            '<circle cx="0" cy="0" r="100" stroke="currentColor" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
            '<circle cx="0" cy="0" r="65" stroke="currentColor" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
            '<circle cx="0" cy="0" r="35" stroke="var(--accent)" stroke-opacity="0.4" stroke-width="1" fill="none"/>'
            '<line x1="-160" y1="0" x2="160" y2="0" stroke="currentColor" stroke-opacity="0.3" stroke-width="1" stroke-dasharray="4 4"/>'
            '<line x1="0" y1="-160" x2="0" y2="160" stroke="currentColor" stroke-opacity="0.3" stroke-width="1" stroke-dasharray="4 4"/>'
            '<line x1="-120" y1="-120" x2="120" y2="120" stroke="currentColor" stroke-opacity="0.2" stroke-width="1" stroke-dasharray="3 3"/>'
            '<line x1="-120" y1="120" x2="120" y2="-120" stroke="currentColor" stroke-opacity="0.2" stroke-width="1" stroke-dasharray="3 3"/>'
            '<!-- Monogram / Emblem Motif -->'
            '<path d="M 0 -85 L 60 20 L 0 50 L -60 20 Z" stroke="var(--accent)" stroke-width="2.4" fill="none"/>'
            '<path d="M 0 -85 L 0 50" stroke="var(--accent)" stroke-width="1.6"/>'
            '</g>'
            '<!-- Typography Baseline Guides -->'
            '<line x1="120" y1="390" x2="680" y2="390" stroke="var(--accent)" stroke-opacity="0.5" stroke-width="1"/>'
            '<line x1="120" y1="410" x2="680" y2="410" stroke="currentColor" stroke-opacity="0.3" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<text x="130" y="385" font-family="monospace" font-size="9" fill="var(--accent-text)">CAP HEIGHT 48px</text>'
            '<text x="130" y="422" font-family="monospace" font-size="9" fill="var(--ink-3)">BASELINE</text>'
            '<!-- Palette Swatches -->'
            '<g transform="translate(640, 140)">'
            '<circle cx="0" cy="0" r="16" fill="#d9822b" stroke="var(--line)" stroke-width="1"/>'
            '<circle cx="0" cy="45" r="16" fill="#2a3a40" stroke="var(--line)" stroke-width="1"/>'
            '<circle cx="0" cy="90" r="16" fill="#e9e5dc" stroke="var(--line)" stroke-width="1"/>'
            '<circle cx="0" cy="135" r="16" fill="#0a0c0e" stroke="var(--line)" stroke-width="1"/>'
            '<text x="26" y="5" font-family="monospace" font-size="9" fill="var(--ink-3)">TERRACOTTA</text>'
            '<text x="26" y="50" font-family="monospace" font-size="9" fill="var(--ink-3)">SLATE CHARCOAL</text>'
            '<text x="26" y="95" font-family="monospace" font-size="9" fill="var(--ink-3)">WARM SAND</text>'
            '<text x="26" y="140" font-family="monospace" font-size="9" fill="var(--ink-3)">OBSIDIAN</text>'
            '</g>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">GEOMETRIC IDENTITY GRID · CHROMATIC MATRIX · NAS-IDE</text>'
        )
    elif slug == 'landscape':
        shapes = (
            '<!-- Master Landscape Plan Perimeter -->'
            '<rect x="150" y="80" width="500" height="340" stroke="currentColor" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
            '<!-- Villa Architectural Footprint -->'
            '<path d="M 200 130 L 420 130 L 420 290 L 320 290 L 320 230 L 200 230 Z" stroke="currentColor" stroke-width="1.8" fill="var(--surface)" fill-opacity="0.9"/>'
            '<text x="290" y="195" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">VILLA ENVELOPE</text>'
            '<!-- Swimming Pool & Water Contours -->'
            '<rect x="460" y="150" width="160" height="90" rx="8" stroke="var(--accent)" stroke-width="1.8" fill="var(--surface)" fill-opacity="0.8"/>'
            '<path d="M 475 180 Q 540 170 605 180 M 475 210 Q 540 200 605 210" stroke="var(--accent)" stroke-opacity="0.5" stroke-width="1.2" fill="none"/>'
            '<text x="540" y="200" font-family="monospace" font-size="10" fill="var(--accent-text)" text-anchor="middle">POOL WATER ELEMENT</text>'
            '<!-- Shaded Pergola -->'
            '<g transform="translate(460, 260)">'
            '<rect width="160" height="80" stroke="currentColor" stroke-width="1.4" fill="none"/>'
            '<line x1="20" y1="0" x2="20" y2="80" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<line x1="50" y1="0" x2="50" y2="80" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<line x1="80" y1="0" x2="80" y2="80" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<line x1="110" y1="0" x2="110" y2="80" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<line x1="140" y1="0" x2="140" y2="80" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2"/>'
            '<text x="80" y="45" font-family="monospace" font-size="9" fill="var(--ink-3)" text-anchor="middle">SHADED PERGOLA</text>'
            '</g>'
            '<!-- Stepping Stones Pathway -->'
            '<circle cx="340" cy="330" r="10" stroke="currentColor" stroke-width="1" fill="none"/>'
            '<circle cx="380" cy="350" r="12" stroke="currentColor" stroke-width="1" fill="none"/>'
            '<circle cx="430" cy="340" r="11" stroke="currentColor" stroke-width="1" fill="none"/>'
            '<!-- Landscape Trees -->'
            '<g transform="translate(230, 350)">'
            '<circle cx="0" cy="0" r="28" stroke="var(--accent)" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.7"/>'
            '<line x1="-10" y1="0" x2="10" y2="0" stroke="var(--accent)" stroke-width="1.2"/>'
            '<line x1="0" y1="-10" x2="0" y2="10" stroke="var(--accent)" stroke-width="1.2"/>'
            '<path d="M 0 -28 C 15 -18 18 -10 28 0 C 18 10 10 18 0 28 C -10 18 -18 10 -28 0 C -18 -10 -10 -18 0 -28" stroke="var(--accent)" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>'
            '</g>'
            '<g transform="translate(600, 110)">'
            '<circle cx="0" cy="0" r="22" stroke="var(--accent)" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.7"/>'
            '<line x1="-8" y1="0" x2="8" y2="0" stroke="var(--accent)" stroke-width="1.2"/>'
            '<line x1="0" y1="-8" x2="0" y2="8" stroke="var(--accent)" stroke-width="1.2"/>'
            '</g>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">LANDSCAPE MASTER PLAN · HARDSCAPE &amp; BIOPHILIC DESIGN · 1:200</text>'
        )
    else:  # supervision
        shapes = (
            '<!-- Structural Grid Lines -->'
            '<line x1="160" y1="110" x2="640" y2="110" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<line x1="160" y1="210" x2="640" y2="210" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<line x1="160" y1="310" x2="640" y2="310" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<line x1="200" y1="80" x2="200" y2="340" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<line x1="360" y1="80" x2="360" y2="340" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<line x1="520" y1="80" x2="520" y2="340" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>'
            '<!-- Grid Axis Bubbles -->'
            '<circle cx="200" cy="65" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="200" y="69" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">A</text>'
            '<circle cx="360" cy="65" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="360" y="69" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">B</text>'
            '<circle cx="520" cy="65" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="520" y="69" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">C</text>'
            '<circle cx="140" cy="110" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="140" y="114" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">1</text>'
            '<circle cx="140" cy="210" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="140" y="214" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">2</text>'
            '<circle cx="140" cy="310" r="12" stroke="currentColor" stroke-width="1.2" fill="var(--surface)"/><text x="140" y="314" font-family="monospace" font-size="10" fill="var(--ink)" text-anchor="middle">3</text>'
            '<!-- Structural Column Markers at Intersections -->'
            '<rect x="194" y="104" width="12" height="12" fill="var(--accent)"/>'
            '<rect x="354" y="104" width="12" height="12" fill="currentColor"/>'
            '<rect x="514" y="104" width="12" height="12" fill="currentColor"/>'
            '<rect x="194" y="204" width="12" height="12" fill="currentColor"/>'
            '<rect x="354" y="204" width="12" height="12" fill="var(--accent)"/>'
            '<rect x="514" y="204" width="12" height="12" fill="currentColor"/>'
            '<rect x="194" y="304" width="12" height="12" fill="currentColor"/>'
            '<rect x="354" y="304" width="12" height="12" fill="currentColor"/>'
            '<rect x="514" y="304" width="12" height="12" fill="var(--accent)"/>'
            '<!-- Inspection Loupe & Reticle Target -->'
            '<g transform="translate(360, 210)">'
            '<circle cx="0" cy="0" r="50" stroke="var(--accent)" stroke-width="1.6" fill="var(--surface)" fill-opacity="0.8"/>'
            '<line x1="-60" y1="0" x2="60" y2="0" stroke="var(--accent)" stroke-width="1" stroke-dasharray="2 2"/>'
            '<line x1="0" y1="-60" x2="0" y2="60" stroke="var(--accent)" stroke-width="1" stroke-dasharray="2 2"/>'
            '<circle cx="0" cy="0" r="25" stroke="var(--accent)" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>'
            '</g>'
            '<!-- Quality Inspection Stamp Card -->'
            '<g transform="translate(480, 340)">'
            '<rect width="240" height="75" rx="8" stroke="var(--accent)" stroke-width="1.4" fill="var(--surface)" fill-opacity="0.95"/>'
            '<text x="120" y="28" font-family="monospace" font-size="11" font-weight="bold" fill="var(--accent-text)" text-anchor="middle">SITE QA/QC AUDIT: PASSED</text>'
            '<text x="120" y="48" font-family="monospace" font-size="9" fill="var(--ink-2)" text-anchor="middle">AXIS TOLERANCE: ±1.5 mm (APPROVED)</text>'
            '<text x="120" y="64" font-family="monospace" font-size="8" fill="var(--ink-3)" text-anchor="middle">NORA ALSAUD SITE CONTROLLER</text>'
            '</g>'
            '<text x="400" y="475" font-family="monospace" font-size="11" fill="var(--ink-3)" text-anchor="middle">STRUCTURAL COORDINATION GRID &amp; SITE EXECUTION CONTROL</text>'
        )
        
    return f'<svg class="blueprint-svg" viewBox="0 0 800 500" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">{grid}{shapes}</svg>'

def page_service_detail(lang, slug):
    t = C[lang]; d = SERV_DETAIL[lang][slug]; ui = t['ui']
    n, _ = SERV[lang][slug]
    key = f'service_{slug}'
    
    crumbs_html = f'''<ol class="crumbs" aria-label="Breadcrumb">
  <li><a href="{PATH[lang]['home']}">{e(t['ui']['home'])}</a></li>
  <li><a href="{PATH[lang]['services']}">{e(t['nav']['services'])}</a></li>
  <li aria-current="page">{e(n)}</li>
</ol>'''

    hero = f'''<section class="phero"><div class="wrap">
  {crumbs_html}
  <span class="eyebrow">{e(ui['service_eyebrow'])}</span>
  <h1 class="h-xl">{d['h1']}</h1>
  <p class="lede">{e(d['lede'])}</p>
</div></section>'''

    bp_svg = blueprint_svg(slug, lang)
    visual = f'''<div class="svc-visual glass rv">
  {bp_svg}
  <div class="svc-visual-bar">
    <span class="svc-visual-tag">{e(d['badge'])}</span>
    <span class="svc-visual-meta">{e(d['ref'])}</span>
  </div>
</div>'''

    proj_btn = f'<p style="margin-block-start:2rem"><a class="link-arrow" href="{PATH[lang]["projects"]}">{e(ui["related"])}{ARROW}</a></p>' if slug in ('architecture', 'interiors', 'furniture') else ''

    overview = f'''<section class="section" style="padding-block-start:0"><div class="wrap svc-detail-split">
  <div class="svc-overview rv">
    <span class="eyebrow">{e(ui['service_eyebrow'])} · {e(n)}</span>
    <h2 class="h-lg" style="margin-block:1rem 1.4rem">{e(d['overview_h'])}</h2>
    <div class="svc-prose">
      <p>{e(d['p1'])}</p>
      <p>{e(d['p2'])}</p>
    </div>
    {proj_btn}
  </div>
  <div class="svc-visual-col rv" style="--d:.1s">
    {visual}
  </div>
</div></section>'''

    deliv_cards = ''.join(
        f'<div class="deliv-card glass rv" style="--d:{idx*.05:.2f}s"><span class="deliv-n">{num}</span><h3>{e(title)}</h3><p>{e(desc)}</p></div>'
        for idx, (num, title, desc) in enumerate(d['deliv'], 1)
    )
    deliv_sec = f'''<section class="section" style="padding-block-start:0"><div class="wrap">
  <div class="sec-head">
    <div class="rv"><span class="eyebrow">{e(ui['deliv_eyebrow'])}</span><h2 class="h-lg" style="margin-block-start:1rem">{e(ui['deliv_heading'])}</h2></div>
    <p class="lede rv" style="--d:.1s">{e(ui['deliv_lede'])}</p>
  </div>
  <div class="deliv-grid">{deliv_cards}</div>
</div></section>'''

    proc_steps = ''.join(
        f'<li class="step rv" style="--d:{idx*.05:.2f}s"><span class="step-n">0{idx}</span><h3>{e(title)}</h3><p>{e(desc)}</p></li>'
        for idx, (title, desc) in enumerate(d['steps'], 1)
    )
    proc_sec = f'''<section class="section" style="padding-block-start:0"><div class="wrap">
  <div class="sec-head">
    <div class="rv"><span class="eyebrow">{e(ui['proc_eyebrow'])}</span><h2 class="h-lg" style="margin-block-start:1rem">{e(ui['proc_heading'])}</h2></div>
    <p class="lede rv" style="--d:.1s">{e(ui['proc_lede'])}</p>
  </div>
  <ol class="steps steps-4">{proc_steps}</ol>
</div></section>'''

    main = hero + overview + deliv_sec + proc_sec + cta_html(lang)
    
    extra_ld = [{
        '@type': 'Service',
        '@id': url(lang, key) + '#service',
        'name': n,
        'description': t['meta'][key][1],
        'provider': {'@id': f'{BASE}/#organization'},
        'serviceType': n,
        'areaServed': {'@type': 'Country', 'name': 'Saudi Arabia'}
    }]
    
    return shell(lang, key, main, extra_ld=extra_ld)

PRJ_PAGE = {
 'en': dict(eyebrow='Projects', h1='Residential and <em>commercial</em> work.', lede='Interior projects shown as design visualisations.',
            note='Images are design visualisations (3D renders) of residential and commercial interiors.'),
 'ar': dict(eyebrow='مشاريعنا', h1='أعمال <em>سكنية</em> وتجارية.', lede='مشاريع داخلية معروضة كتصورات تصميمية.',
            note='الصور تصورات تصميمية (رسومات ثلاثية الأبعاد) لمساحات داخلية سكنية وتجارية.'),
}

def page_projects(lang):
    t = C[lang]; p = PRJ_PAGE[lang]; ui = t['ui']; suf = CAP_SUFFIX[lang]
    nres = sum(1 for x in PROJECTS if x[1] == 'residential'); ncom = len(PROJECTS) - nres
    items = []
    for k, cat, en_c, ar_c in PROJECTS:
        c = en_c if lang == 'en' else ar_c
        alt = f'{c} — {suf}'
        items.append(f'<li class="pitem" data-cat="{cat}"><button type="button" data-full="{full_src(k)}" data-alt="{e(alt)}" data-cap="{e(c)}" aria-label="{e(c)}">{img(k, alt, "", "(min-width:1040px) 33vw, (min-width:640px) 50vw, 100vw")}<span class="work-cap glass"><span>{e(c)}</span><small>{e(ui[cat])}</small></span></button></li>')
    ld = [{'@type': 'ImageGallery', '@id': url(lang, 'projects') + '#gallery', 'name': t['meta']['projects'][0], 'inLanguage': lang,
           'image': [{'@type': 'ImageObject', 'contentUrl': BASE + full_src(k), 'name': (en_c if lang == 'en' else ar_c), 'caption': f'{(en_c if lang == "en" else ar_c)} — {suf}', 'representativeOfPage': False} for k, _, en_c, ar_c in PROJECTS]}]
    main = f'''{phero(lang, 'projects', p['eyebrow'], p['h1'], p['lede'])}
<section class="section" style="padding-block-start:1rem"><div class="wrap">
  <div class="filters glass" role="group" aria-label="{e(ui['filter'])}">
    <button type="button" data-filter="all" aria-pressed="true">{e(ui['all'])}<small>{len(PROJECTS)}</small></button>
    <button type="button" data-filter="residential" aria-pressed="false">{e(ui['residential'])}<small>{nres}</small></button>
    <button type="button" data-filter="commercial" aria-pressed="false">{e(ui['commercial'])}<small>{ncom}</small></button>
  </div>
  <p class="vh" id="filter-live" role="status" aria-live="polite"></p>
  <ul class="pgrid">{"".join(items)}</ul>
  <p class="note">{e(p['note'])}</p>
</div></section>
<dialog class="lb" aria-label="{e(ui['gallery'])}">
  <button class="lb-btn lb-close glass" type="button" aria-label="{e(ui['close'])}">{CLOSE}</button>
  <button class="lb-btn lb-prev glass" type="button" aria-label="{e(ui['prev'])}">{CHEV}</button>
  <button class="lb-btn lb-next glass" type="button" aria-label="{e(ui['next'])}">{CHEV}</button>
  <figure class="lb-fig"><img alt="" width="1600" height="1200" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><figcaption class="lb-cap glass"><b class="lb-t"></b><span class="lb-n"></span></figcaption></figure>
</dialog>
{cta_html(lang)}
'''
    return shell(lang, 'projects', main, ld)

# ---- forms
def field(label, name, typ='text', req=False, full=False, ph='', ac='', ltr=False, ui_req=''):
    star = f' <span class="req" aria-hidden="true">*</span>' if req else ''
    attrs = (' required' if req else '') + (' autocomplete="%s"' % ac if ac else '') + (' dir="ltr"' if ltr else '') + (' placeholder="%s"' % e(ph) if ph else '')
    return f'<div class="field{" full" if full else ""}"><label for="f-{name}">{e(label)}{star}</label><input class="input" id="f-{name}" name="{name}" type="{typ}"{attrs}></div>'

def area(label, name, req=False):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    return f'<div class="field full"><label for="f-{name}">{e(label)}{star}</label><textarea class="input" id="f-{name}" name="{name}" rows="4"{" required" if req else ""}></textarea></div>'

def chips(label, name, opts, req=False, full=True):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    cs = ''.join(f'<label class="chip"><input type="radio" name="{name}" value="{e(v)}"{" required" if req else ""}><span>{e(txt)}</span></label>' for v, txt in opts)
    return f'<div class="field{" full" if full else ""}" role="radiogroup" aria-label="{e(label)}"><span class="lbl">{e(label)}{star}</span><div class="chips">{cs}</div></div>'

FORMS = {
 'en': dict(
    c_name='Name', c_email='Email', c_phone='Phone', c_type='Project type', c_msg='Message', types=[('residential', 'Residential'), ('commercial', 'Commercial'), ('other', 'Other')],
    j_name='Name', j_email='Email', j_mobile='Mobile number', j_gender='Gender', genders=[('female', 'Female'), ('male', 'Male')],
    j_nat='Nationality', nats=[('saudi', 'Saudi Arabian'), ('non-saudi', 'Non-Saudi')],
    j_edu='Education', edus=[('associate', 'Associate degree'), ('bachelor', 'Bachelor’s degree'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')],
    j_qual='Qualification', j_port='Portfolio website', j_job='Job details', jobs=[('full-time', 'Full time'), ('part-time', 'Part time'), ('internship', 'Internship'), ('volunteering', 'Volunteering')],
    j_for='Applying for', j_msg='Message', j_cv='CV or portfolio (PDF, DOC; max 5 MB)',
    req_note='Fields marked * are required.'),
 'ar': dict(
    c_name='الاسم', c_email='البريد الإلكتروني', c_phone='رقم الجوال', c_type='نوع المشروع', c_msg='الرسالة', types=[('residential', 'سكني'), ('commercial', 'تجاري'), ('other', 'أخرى')],
    j_name='الاسم', j_email='البريد الإلكتروني', j_mobile='رقم الجوال', j_gender='الجنس', genders=[('female', 'أنثى'), ('male', 'ذكر')],
    j_nat='الجنسية', nats=[('saudi', 'سعودي/ـة'), ('non-saudi', 'غير سعودي/ـة')],
    j_edu='التعليم', edus=[('associate', 'الزمالة'), ('bachelor', 'بكالوريوس'), ('undergraduate', 'المرحلة الجامعية'), ('postgraduate', 'دراسات عليا')],
    j_qual='المؤهل العلمي', j_port='نماذج من الأعمال (رابط)', j_job='تفاصيل الوظيفة', jobs=[('full-time', 'دوام كامل'), ('part-time', 'دوام جزئي'), ('internship', 'تدريب'), ('volunteering', 'تطوع')],
    j_for='التقدم لـ', j_msg='رسالة', j_cv='السيرة الذاتية أو نماذج الأعمال (PDF أو DOC، بحد أقصى 5 ميجابايت)',
    req_note='الحقول المميزة بعلامة * مطلوبة.'),
}

def page_careers(lang):
    t = C[lang]; F = FORMS[lang]; ui = t['ui']
    copy = {'en': ('Careers', 'Join <em>us</em>.', 'Interested in working with the team? Tell us about yourself and share your portfolio.'),
            'ar': ('انضم إلينا', 'انضم <em>إلينا</em>.', 'هل ترغب بالعمل مع الفريق؟ عرّفنا بنفسك وشاركنا نماذج من أعمالك.')}[lang]
    form = f'''<form class="form-card glass rv" data-form data-endpoint="" action="" method="post" enctype="multipart/form-data" novalidate aria-label="{e(copy[0])}">
  <div class="fgrid two">
    {field(F['j_name'], 'name', req=True, ac='name')}
    {field(F['j_email'], 'email', 'email', req=True, ac='email', ltr=True)}
    {field(F['j_mobile'], 'mobile', 'tel', req=True, ac='tel', ltr=True)}
    {field(F['j_qual'], 'qualification')}
    {chips(F['j_gender'], 'gender', F['genders'], True, False)}
    {chips(F['j_nat'], 'nationality', F['nats'], True, False)}
    {chips(F['j_edu'], 'education', F['edus'], True)}
    {chips(F['j_job'], 'job_type', F['jobs'], True)}
    {field(F['j_for'], 'applying_for')}
    {field(F['j_port'], 'portfolio', 'url', ltr=True, ph='https://')}
    {area(F['j_msg'], 'message')}
    <div class="field full"><label for="f-cv">{e(F['j_cv'])}</label><input class="file-in" id="f-cv" name="cv" type="file" accept=".pdf,.doc,.docx"></div>
    <div class="hp" aria-hidden="true"><label>Website<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></div>
  </div>
  <div class="form-foot"><button class="btn btn-solid" type="submit">{e(ui['apply'])}{ARROW}</button><span class="hint">{e(F['req_note'])}</span></div>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>'''
    main = f'''<section class="phero"><div class="wrap">
  <ol class="crumbs" aria-label="Breadcrumb"><li><a href="{PATH[lang]['home']}">{e(ui['home'])}</a></li><li aria-current="page">{e(t['nav']['careers'])}</li></ol>
</div></section>
<section class="section" style="padding-block-start:0"><div class="wrap split">
  <div><span class="eyebrow">{e(copy[0])}</span><h1 class="h-xl" style="margin-block:1.2rem 1.4rem;font-size:clamp(2.4rem,5vw,4.4rem)">{copy[1]}</h1><p class="lede">{e(copy[2])}</p></div>
  <div>{form}</div>
</div></section>
'''
    return shell(lang, 'careers', main)

def page_contact(lang):
    t = C[lang]; F = FORMS[lang]; ui = t['ui']
    copy = {'en': ('Get in touch', 'Let’s talk about <em>your project</em>.', 'Call, email or visit us in Khobar, or send a message below.', 'Phone', 'Email', 'Location', 'Working hours'),
            'ar': ('ابقَ على تواصل معنا', 'لنتحدث عن <em>مشروعك</em>.', 'اتصل بنا أو راسلنا أو زُرنا في الخبر، أو أرسل رسالة أدناه.', 'الهاتف', 'البريد الإلكتروني', 'الموقع', 'ساعات العمل')}[lang]
    cards = f'''<div class="ccards">
  <div class="ccard glass rv"><span class="lbl">{copy[3]}</span><a href="tel:{PHONE_TEL}">{tel_html()}</a></div>
  <div class="ccard glass rv" style="--d:.05s"><span class="lbl">{copy[4]}</span><a href="mailto:{EMAIL}"><bdi dir="ltr">{EMAIL}</bdi></a></div>
  <div class="ccard glass wide rv" style="--d:.1s"><span class="lbl">{copy[5]}</span><p>{e(t['address'])}</p><a class="link-arrow" href="{MAPS}" target="_blank" rel="noopener">{e(ui['open_maps'])}{ARROW}</a></div>
  <div class="ccard glass wide rv" style="--d:.15s"><span class="lbl">{copy[6]}</span><p>{e(t['days'])}</p><small>{e(t['hours'])}</small></div>
</div>'''
    form = f'''<form class="form-card glass rv" data-form data-endpoint="" action="" method="post" novalidate aria-label="{e(copy[0])}" style="margin-block-start:1.5rem">
  <div class="fgrid two">
    {field(F['c_name'], 'name', req=True, ac='name')}
    {field(F['c_email'], 'email', 'email', req=True, ac='email', ltr=True)}
    {field(F['c_phone'], 'phone', 'tel', ac='tel', ltr=True)}
    {chips(F['c_type'], 'project_type', F['types'], False, False)}
    {area(F['c_msg'], 'message', True)}
    <div class="hp" aria-hidden="true"><label>Website<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></div>
  </div>
  <div class="form-foot"><button class="btn btn-solid" type="submit">{e(ui['send'])}{ARROW}</button><span class="hint">{e(F['req_note'])}</span></div>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>'''
    main = f'''{phero(lang, 'contact', copy[0], copy[1], copy[2])}
<section class="section" style="padding-block-start:1rem"><div class="wrap split">
  <div style="position:static">{cards}</div>
  <div>{form}</div>
</div></section>
'''
    return shell(lang, 'contact', main)

def page_404():
    lang = 'ar'; t = C[lang]
    main = f'''<section class="nf"><div class="wrap"><span class="eyebrow">404</span><h1 class="h-xl" style="margin-block:1.2rem">الصفحة <em>غير موجودة</em>.</h1>
<p class="lede" style="margin-inline:auto">ربما تم نقل الصفحة أو لم تعد متوفرة. يمكنك العودة إلى الصفحة الرئيسية أو استعراض مشاريعنا.</p>
<div class="cta-row" style="justify-content:center"><a class="btn btn-solid" href="/">{e(t['ui']['home'])}{ARROW}</a><a class="btn btn-ghost" href="/projects/">{e(t['nav']['projects'])}</a><a class="btn btn-ghost" href="/en/" lang="en" hreflang="en">English</a></div></div></section>'''
    return shell(lang, 'home', main, noindex=True, canonical=BASE + '/404.html', title='الصفحة غير موجودة | نورة السعود معماريون ومهندسون', desc='الصفحة غير موجودة.')

# ---------------------------------------------------------------- write
BUILDERS = {'home': page_home, 'about': page_about, 'services': page_services, 'projects': page_projects, 'careers': page_careers, 'contact': page_contact}

def write(path, content):
    full = f'{SITE}{path}'
    if path.endswith('/'):
        full += 'index.html'
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)

def clean_site():
    if not os.path.exists(SITE):
        return
    for item in os.listdir(SITE):
        if item in ('assets', '.htaccess'):
            continue
        full = os.path.join(SITE, item)
        try:
            if os.path.isdir(full):
                for root_dir, dirs, files in os.walk(full, topdown=False):
                    for file in files:
                        fp = os.path.join(root_dir, file)
                        try:
                            os.chmod(fp, stat.S_IWRITE)
                            os.remove(fp)
                        except Exception:
                            pass
                    for d in dirs:
                        dp = os.path.join(root_dir, d)
                        try:
                            os.rmdir(dp)
                        except Exception:
                            pass
                try:
                    os.rmdir(full)
                except Exception:
                    pass
            else:
                os.chmod(full, stat.S_IWRITE)
                os.remove(full)
        except Exception:
            pass

def main():
    clean_site()
    for lang in ('ar', 'en'):
        for key in PAGES:
            write(PATH[lang][key], BUILDERS[key](lang))
        for slug in SERV_SLUGS:
            write(PATH[lang][f'service_{slug}'], page_service_detail(lang, slug))
    write('/404.html', page_404())
    # sitemap with hreflang alternates
    all_keys = list(PAGES) + [f'service_{s}' for s in SERV_SLUGS]
    urls = []
    for key in all_keys:
        for lang in ('en', 'ar'):
            alt = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, key)}"/>' for l in ('ar', 'en')) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("ar", key)}"/>'
            pri = '1.0' if key == 'home' else ('0.8' if (key in ('services', 'projects') or key.startswith('service_')) else '0.6')
            urls.append(f'<url><loc>{url(lang, key)}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority>{alt}</url>')
    open(f'{SITE}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
    open(f'{SITE}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    llms_ar_svc = '\n'.join(f"  - [{SERV['ar'][s][0]}]({url('ar', f'service_{s}')})" for s in SERV_SLUGS)
    llms_en_svc = '\n'.join(f"  - [{SERV['en'][s][0]}]({url('en', f'service_{s}')})" for s in SERV_SLUGS)
    llms = f'''# {C['ar']['name']} — {C['en']['name']}

> مكتب هندسي وتصميم في الخبر، المملكة العربية السعودية، يقدم خدمات التصميم المعماري والتصميم الداخلي وتصميم الأثاث والهوية والعلامة التجارية والحدائق والإشراف والتنفيذ. الموقع متوفر باللغتين العربية والإنجليزية.
> Engineering and design office in Khobar, Saudi Arabia, offering architecture, interiors, furniture design, identity & branding, landscape, and project supervision & execution. Site available in Arabic and English.

## Key facts / معلومات رئيسية
- Address / العنوان: {C['ar']['address']} ({C['en']['address']})
- Phone / الهاتف: {PHONE_DISP}
- Email / البريد الإلكتروني: {EMAIL}
- Working hours / ساعات العمل: {C['ar']['days']}، {C['ar']['hours']}

## الصفحات (بالعربية - افتراضي)
- [الرئيسية]({url('ar','home')}): نظرة عامة
- [من نحن]({url('ar','about')}): عن المكتب ورؤيته
- [خدماتنا]({url('ar','services')}): الخدمات الست
{llms_ar_svc}
- [مشاريعنا]({url('ar','projects')}): تصورات تصميمية لمشاريع سكنية وتجارية
- [انضم إلينا]({url('ar','careers')}): نموذج التقديم والتوظيف
- [اتصل بنا]({url('ar','contact')}): الهاتف والبريد والموقع وساعات العمل

## Pages (English)
- [Home]({url('en','home')}): overview
- [About]({url('en','about')}): the office and its vision
- [Services]({url('en','services')}): the six disciplines
{llms_en_svc}
- [Projects]({url('en','projects')}): residential and commercial interior visualisations
- [Join us]({url('en','careers')}): application form
- [Contact]({url('en','contact')}): phone, email, location, hours
'''
    open(f'{SITE}/llms.txt', 'w', encoding='utf-8').write(llms)
    total_built = (len(PAGES) + len(SERV_SLUGS)) * 2 + 1
    print('built', total_built, 'pages')

if __name__ == '__main__':
    main()
