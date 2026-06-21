from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object="config.Config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.assets import assets_bp
    from app.routes.risks import risks_bp
    from app.routes.policies import policies_bp
    from app.routes.incidents import incidents_bp
    from app.routes.controls import controls_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(assets_bp, url_prefix="/assets")
    app.register_blueprint(risks_bp, url_prefix="/risks")
    app.register_blueprint(policies_bp, url_prefix="/policies")
    app.register_blueprint(incidents_bp, url_prefix="/incidents")
    app.register_blueprint(controls_bp, url_prefix="/controls")

    with app.app_context():
        db.create_all()
        _seed_controls()

    return app


def _seed_controls():
    from app.models import Control

    if Control.query.count() > 0:
        return

    annex_a_controls = [
        # A.5 - Bilgi Güvenliği Politikaları
        ("A.5.1.1", "Bilgi güvenliği için politikalar", "A.5 Bilgi Güvenliği Politikaları"),
        ("A.5.1.2", "Bilgi güvenliği politikalarının gözden geçirilmesi", "A.5 Bilgi Güvenliği Politikaları"),
        # A.6 - Bilgi Güvenliğinin Organizasyonu
        ("A.6.1.1", "Bilgi güvenliği rolleri ve sorumlulukları", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.1.2", "Görevler ayrılığı", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.1.3", "İlgili makamlarla iletişim", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.1.4", "Özel ilgi gruplarıyla iletişim", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.1.5", "Proje yönetiminde bilgi güvenliği", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.2.1", "Mobil cihaz politikası", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        ("A.6.2.2", "Uzaktan çalışma", "A.6 Bilgi Güvenliğinin Organizasyonu"),
        # A.7 - İnsan Kaynakları Güvenliği
        ("A.7.1.1", "Tarama", "A.7 İnsan Kaynakları Güvenliği"),
        ("A.7.1.2", "İstihdam hüküm ve koşulları", "A.7 İnsan Kaynakları Güvenliği"),
        ("A.7.2.1", "Yönetim sorumlulukları", "A.7 İnsan Kaynakları Güvenliği"),
        ("A.7.2.2", "Bilgi güvenliği farkındalığı, eğitimi ve öğretimi", "A.7 İnsan Kaynakları Güvenliği"),
        ("A.7.2.3", "Disiplin süreci", "A.7 İnsan Kaynakları Güvenliği"),
        ("A.7.3.1", "İstihdam sona erme veya değişiklik sorumlulukları", "A.7 İnsan Kaynakları Güvenliği"),
        # A.8 - Varlık Yönetimi
        ("A.8.1.1", "Varlıkların envanteri", "A.8 Varlık Yönetimi"),
        ("A.8.1.2", "Varlıkların sahipliği", "A.8 Varlık Yönetimi"),
        ("A.8.1.3", "Varlıkların kabul edilebilir kullanımı", "A.8 Varlık Yönetimi"),
        ("A.8.1.4", "Varlıkların iadesi", "A.8 Varlık Yönetimi"),
        ("A.8.2.1", "Bilginin sınıflandırılması", "A.8 Varlık Yönetimi"),
        ("A.8.2.2", "Bilginin etiketlenmesi", "A.8 Varlık Yönetimi"),
        ("A.8.2.3", "Varlıkların işlenmesi", "A.8 Varlık Yönetimi"),
        ("A.8.3.1", "Taşınabilir ortam yönetimi", "A.8 Varlık Yönetimi"),
        ("A.8.3.2", "Ortamın imhası", "A.8 Varlık Yönetimi"),
        ("A.8.3.3", "Fiziksel ortam transferi", "A.8 Varlık Yönetimi"),
        # A.9 - Erişim Kontrolü
        ("A.9.1.1", "Erişim kontrolü politikası", "A.9 Erişim Kontrolü"),
        ("A.9.1.2", "Ağlara ve ağ hizmetlerine erişim", "A.9 Erişim Kontrolü"),
        ("A.9.2.1", "Kullanıcı kayıt ve silme", "A.9 Erişim Kontrolü"),
        ("A.9.2.2", "Kullanıcı erişim sağlama", "A.9 Erişim Kontrolü"),
        ("A.9.2.3", "Ayrıcalıklı erişim haklarının yönetimi", "A.9 Erişim Kontrolü"),
        ("A.9.2.4", "Gizli kimlik doğrulama bilgisinin yönetimi", "A.9 Erişim Kontrolü"),
        ("A.9.2.5", "Kullanıcı erişim haklarının gözden geçirilmesi", "A.9 Erişim Kontrolü"),
        ("A.9.2.6", "Erişim haklarının kaldırılması veya ayarlanması", "A.9 Erişim Kontrolü"),
        ("A.9.3.1", "Gizli kimlik doğrulama bilgisinin kullanımı", "A.9 Erişim Kontrolü"),
        ("A.9.4.1", "Bilgiye erişim kısıtlama", "A.9 Erişim Kontrolü"),
        ("A.9.4.2", "Güvenli oturum açma prosedürleri", "A.9 Erişim Kontrolü"),
        ("A.9.4.3", "Parola yönetim sistemi", "A.9 Erişim Kontrolü"),
        ("A.9.4.4", "Ayrıcalıklı yardımcı program kullanımı", "A.9 Erişim Kontrolü"),
        ("A.9.4.5", "Program kaynak koduna erişim kontrolü", "A.9 Erişim Kontrolü"),
        # A.10 - Kriptografi
        ("A.10.1.1", "Kriptografik kontrollerin kullanımına ilişkin politika", "A.10 Kriptografi"),
        ("A.10.1.2", "Anahtar yönetimi", "A.10 Kriptografi"),
        # A.11 - Fiziksel ve Çevresel Güvenlik
        ("A.11.1.1", "Fiziksel güvenlik çevresi", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.1.2", "Fiziksel giriş kontrolleri", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.1.3", "Ofislerin, odaların ve tesislerin güvenliği", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.1.4", "Dış ve çevresel tehditlerden korunma", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.1.5", "Güvenli alanlarda çalışma", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.1.6", "Teslimat ve yükleme alanları", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.1", "Ekipman yerleştirme ve koruma", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.2", "Destekleyici servisler", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.3", "Kablo güvenliği", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.4", "Ekipman bakımı", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.5", "Varlıkların kaldırılması", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.6", "Tesis dışındaki ekipman ve varlıkların güvenliği", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.7", "Güvenli imha veya yeniden kullanım", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.8", "Gözetimsiz kullanıcı ekipmanı", "A.11 Fiziksel ve Çevresel Güvenlik"),
        ("A.11.2.9", "Temiz masa ve temiz ekran politikası", "A.11 Fiziksel ve Çevresel Güvenlik"),
        # A.12 - Operasyon Güvenliği
        ("A.12.1.1", "Dokümante edilmiş operasyon prosedürleri", "A.12 Operasyon Güvenliği"),
        ("A.12.1.2", "Değişiklik yönetimi", "A.12 Operasyon Güvenliği"),
        ("A.12.1.3", "Kapasite yönetimi", "A.12 Operasyon Güvenliği"),
        ("A.12.1.4", "Geliştirme, test ve operasyon ortamlarının ayrımı", "A.12 Operasyon Güvenliği"),
        ("A.12.2.1", "Kötü amaçlı yazılımlara karşı kontroller", "A.12 Operasyon Güvenliği"),
        ("A.12.3.1", "Bilgi yedekleme", "A.12 Operasyon Güvenliği"),
        ("A.12.4.1", "Olay kayıt", "A.12 Operasyon Güvenliği"),
        ("A.12.4.2", "Kayıt bilgisinin korunması", "A.12 Operasyon Güvenliği"),
        ("A.12.4.3", "Yönetici ve operatör kayıtları", "A.12 Operasyon Güvenliği"),
        ("A.12.4.4", "Saat senkronizasyonu", "A.12 Operasyon Güvenliği"),
        ("A.12.5.1", "Operasyonel sistemlere yazılım kurulumu", "A.12 Operasyon Güvenliği"),
        ("A.12.6.1", "Teknik güvenlik açıklarının yönetimi", "A.12 Operasyon Güvenliği"),
        ("A.12.6.2", "Yazılım kurulumuna yönelik kısıtlamalar", "A.12 Operasyon Güvenliği"),
        ("A.12.7.1", "Bilgi sistemleri denetim kontrolleri", "A.12 Operasyon Güvenliği"),
        # A.13 - İletişim Güvenliği
        ("A.13.1.1", "Ağ kontrolleri", "A.13 İletişim Güvenliği"),
        ("A.13.1.2", "Ağ hizmetleri güvenliği", "A.13 İletişim Güvenliği"),
        ("A.13.1.3", "Ağlarda ayrım", "A.13 İletişim Güvenliği"),
        ("A.13.2.1", "Bilgi transfer politikaları ve prosedürleri", "A.13 İletişim Güvenliği"),
        ("A.13.2.2", "Bilgi transfer anlaşmaları", "A.13 İletişim Güvenliği"),
        ("A.13.2.3", "Elektronik mesajlaşma", "A.13 İletişim Güvenliği"),
        ("A.13.2.4", "Gizlilik veya ifşa etmeme anlaşmaları", "A.13 İletişim Güvenliği"),
        # A.14 - Sistem Edinimi, Geliştirme ve Bakımı
        ("A.14.1.1", "Bilgi güvenliği gereksinimlerinin analizi ve spesifikasyonu", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.1.2", "Genel hizmetler üzerindeki uygulama hizmetlerinin güvenliği", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.1.3", "Uygulama hizmetleri işlemlerinin korunması", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.1", "Güvenli geliştirme politikası", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.2", "Sistem değişiklik kontrol prosedürleri", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.3", "İşletim platformu değişikliğinden sonra teknik gözden geçirme", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.4", "Yazılım paketlerindeki değişikliklere yönelik kısıtlamalar", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.5", "Güvenli sistem mühendisliği ilkeleri", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.6", "Güvenli geliştirme ortamı", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.7", "Dış kaynaklı geliştirme", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.8", "Sistem güvenliği testleri", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.2.9", "Sistem kabul testleri", "A.14 Sistem Geliştirme ve Bakımı"),
        ("A.14.3.1", "Test verilerinin korunması", "A.14 Sistem Geliştirme ve Bakımı"),
        # A.15 - Tedarikçi İlişkileri
        ("A.15.1.1", "Tedarikçilerle ilgili bilgi güvenliği politikası", "A.15 Tedarikçi İlişkileri"),
        ("A.15.1.2", "Tedarikçi anlaşmalarında güvenliğe değinme", "A.15 Tedarikçi İlişkileri"),
        ("A.15.1.3", "Bilgi ve iletişim teknolojisi tedarik zinciri", "A.15 Tedarikçi İlişkileri"),
        ("A.15.2.1", "Tedarikçi hizmet teslimatının izlenmesi ve gözden geçirilmesi", "A.15 Tedarikçi İlişkileri"),
        ("A.15.2.2", "Tedarikçi hizmetlerindeki değişikliklerin yönetimi", "A.15 Tedarikçi İlişkileri"),
        # A.16 - Bilgi Güvenliği Olay Yönetimi
        ("A.16.1.1", "Sorumluluklar ve prosedürler", "A.16 Olay Yönetimi"),
        ("A.16.1.2", "Bilgi güvenliği olaylarının raporlanması", "A.16 Olay Yönetimi"),
        ("A.16.1.3", "Bilgi güvenliği zayıflıklarının raporlanması", "A.16 Olay Yönetimi"),
        ("A.16.1.4", "Bilgi güvenliği olaylarının değerlendirilmesi ve kararlaştırılması", "A.16 Olay Yönetimi"),
        ("A.16.1.5", "Bilgi güvenliği olaylarına müdahale", "A.16 Olay Yönetimi"),
        ("A.16.1.6", "Bilgi güvenliği olaylarından öğrenme", "A.16 Olay Yönetimi"),
        ("A.16.1.7", "Kanıt toplama", "A.16 Olay Yönetimi"),
        # A.17 - İş Sürekliliği Yönetiminin Bilgi Güvenliği Boyutları
        ("A.17.1.1", "Bilgi güvenliği sürekliliğinin planlanması", "A.17 İş Sürekliliği"),
        ("A.17.1.2", "Bilgi güvenliği sürekliliğinin uygulanması", "A.17 İş Sürekliliği"),
        ("A.17.1.3", "Bilgi güvenliği sürekliliğinin doğrulanması, gözden geçirilmesi ve değerlendirilmesi", "A.17 İş Sürekliliği"),
        ("A.17.2.1", "Bilgi işleme tesislerinin kullanılabilirliği", "A.17 İş Sürekliliği"),
        # A.18 - Uyum
        ("A.18.1.1", "Geçerli mevzuat ve sözleşme gereksinimlerinin belirlenmesi", "A.18 Uyum"),
        ("A.18.1.2", "Fikri mülkiyet hakları", "A.18 Uyum"),
        ("A.18.1.3", "Kayıtların korunması", "A.18 Uyum"),
        ("A.18.1.4", "Kişisel bilgilerin gizliliği ve korunması", "A.18 Uyum"),
        ("A.18.1.5", "Kriptografik kontrollerin düzenlenmesi", "A.18 Uyum"),
        ("A.18.2.1", "Bilgi güvenliğinin bağımsız gözden geçirilmesi", "A.18 Uyum"),
        ("A.18.2.2", "Güvenlik politikaları ve standartlarına uyum", "A.18 Uyum"),
        ("A.18.2.3", "Teknik uyum gözden geçirmesi", "A.18 Uyum"),
    ]

    for ctrl_id, name, category in annex_a_controls:
        ctrl = Control(
            control_id=ctrl_id,
            name=name,
            category=category,
            status="Uygulanmadı",
        )
        db.session.add(ctrl)
    db.session.commit()
