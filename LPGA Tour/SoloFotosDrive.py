import os
import shutil

ORIGEN = 'C:\\NAS_PAU\\TFG\\LPGA\\Instagram'
DESTINO = 'G:\\La meva unitat\\TFG_Instagram\\LPGA'

# Lista de usernames válidos (puedes cargarla desde un archivo si prefieres)
usernames_validos = {
    'a_lim_queen', 'adela_cernousek', 'aditiashok', 'akie.iwai', 'alana_uriell',
    'albanevalenzuela', 'alenasharp07', 'alexampano', 'alexfoersterling',
    'alinekrauter', 'thealisonlee', 'allysoncorpuz', 'a_mc10', 'amandadgolf',
    'amelialewislpga', 'amyyanglpga', 'ana_belac97', 'anapelaezgolf',
    'andrealee', 'angelyin', 'angstanford', 'a_nordqvist', 'annieparkusc',
    'mayariya', 'arpichaya_piano', 'ashbuhaigolf', 'austonkim',
    'ayaka_furue27', 'ayako_uehara.golf', 'azagolf', 'tardy_for_the_party_',
    'benedettamoresco_', 'biancapagda', 'briannagolf', 'brittalto',
    'brittany1golf', 'brontemaylaw', 'brookehendersongolf', 'brooke_matthews1',
    'caley_mcginty', 'carlotagolf', 'caroline_inglis', 'caro_masson_',
    'cassie_porter_', 'celine.borgee', 'celineboutier', 'p_proudly',
    'charley.hull', 'chisato.iwai_101', 'thechristinakim', 'cristiekerr',
    'danafallgolf', 'daniholmqvist', 'ddarquea', 'diac1127', 'daniellekang',
    'dewiweber', 'emilykristinepedersen', 'ertalley', 'esther_hen',
    'eunheeji_lpga', 'fatifcanogolf', 'fionaxu888', 'fridakinhult',
    'gabiruffels', 'gabylopezgolf', 'gemmadryburgh', 'georgiahall23',
    'gigistoll_', 'gracekimmey', 'gurleenkaurgolf', 'haeran_ryu',
    'hannahgreengolf', 'heath.er.lin', 'heeyounglpga', 'pinacoooon',
    'hiraintherough', 'hyejin_choi1', 'hyo_joo_kim', 'joon_jang2003',
    'ilheelee', 'ingeechun_dumbo', 'ina_yoon_global', 'iingridlindblad',
    'isafierro_', 'wannjrv', 'jasmine_lpga', 'jeeno.atthaya', 'jennifer.chang',
    'jenniferkupcho', 'jennifermsong', 'jennybae_golf', 'jenny____coleman',
    'jennyshin_jtibs', 'j.lee5', '__________6ix', 'jessicaporvasnik',
    'jinyoungko_official', 'jingyangolf', 'jiwonjeon_', 'jodi_ewart',
    'juliagolf_12', 'kaitlyn.papp', 'karisdavidson_', 'karrie_webb',
    'kate.stroh', 'kellytan33', 'kiiraolivia', 'kimkaufmangolf',
    'kristengillman', 'laetitiabeck18', 'l_coughlin', 'laurenhartlage',
    'leeannepace', 'leonamaguire', 'lexi', 'liliavu', 'lindseyweaver_',
    'lindyduncan72', 'linngrant', 'linneaasstrom', 'lizettesalas5',
    'lucyli_golf', 'lydsko', 'madelenesagstrom', 'madison_younggolf',
    'majastark1', 'malia.nam', 'mderoey', 'maomao_golf', 'mariafassi1',
    'marifetorres.pr', 'mostacksbirdies', 'mariajogolf', 'marinaaadee',
    'maryliu.611', 'matilda_castren', 'maleblancgolf', 'megan_khang',
    'melreidgolf', 'hyang2golf', 'min_lee_golf', 'minaharigae',
    'minami_katsu', 'minjee27', '__minjikang__', 'mirandaxy11',
    'miyuu_yamashita', 'm_oneinamillion', 'morganemetraux', 'mo_moriya',
    'lilymhe', 'nannakoerstzmadsen', 'narinant_oncodinestrail', 'nasahataoka',
    'gusevatata03', 'sim_nv.golf', 'nellykorda', 'nicolelaarsen', 'nuriaitu',
    'oliviaccowan', 'luvmeawpajaree', 'impattyt', 'paularetosa',
    'pauline_roussinbouchard', 'parinprinp', 'pyc_money', 'pernillagolf',
    'perrinedelacour', 'polly.mack', 'waen_pornanong', 'rio_tkd402',
    'robyn.choi', 'rosezhang', 'ruixinliu_golf', 'ruoningyin1', 'ryannotoole',
    'teba_.425', 'sandragalvez85', 'sarahjanegolf', 'sarah_kempy',
    'sschmelly', 'savannahgrewal_', '1soyeonryu', 'som_time_', 'soobin.joo',
    'sophiacpopov', 'ssuchiacheng', 'steph.kyriacou', 'stephmeadow20',
    'suohgolf', 'xxndl', 'tiffanywbz', 'vickyhurst', 'weilinghsu1994',
    'weiweizhang0315', 'jan_wichanee6395', 'amyyin32', 'janetlinxiyu',
    'yanliu_golf', 'yanitseng', 'yealiminoh', 'yuliu_', 'renyue1218',
    'yukasaso_official', 'yunapan_02', 'yuri_yoshida__'
}

for usuario in os.listdir(ORIGEN):
    if usuario not in usernames_validos:
        continue

    ruta_usuario = os.path.join(ORIGEN, usuario)
    if os.path.isdir(ruta_usuario):
        print(f'🔍 Procesando usuario: {usuario}')
        origen_fotos = os.path.join(ruta_usuario, 'fotos')
        if os.path.exists(origen_fotos):
            destino_usuario = os.path.join(DESTINO, usuario, 'fotos')
            os.makedirs(destino_usuario, exist_ok=True)
            for archivo in os.listdir(origen_fotos):
                if archivo.endswith('_UTC.jpg') or archivo.endswith('_UTC_1.jpg'):
                    ruta_archivo = os.path.join(origen_fotos, archivo)
                    destino_archivo = os.path.join(destino_usuario, archivo)
                    if not os.path.exists(destino_archivo):
                        shutil.copy2(ruta_archivo, destino_archivo)
                        print(f'   ✅ Copiado: {archivo}')
                    else:
                        print(f'   ⚠️ Ya existe: {archivo}')
        print('---')

print("Copia completada. Solo fotos con sufijo _UTC o _UTC_1 se han copiado.")

