from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings

from contact.models import ContactRequest
from core.models import CompanyInfo
from services.models import FleetVehicle, Route, Service

VALID = {'full_name': 'علی رضایی', 'phone': '۰۹۱۲ ۳۴۵ ۶۷۸۹', 'email': 'ali@example.com',
         'origin': 'Istanbul', 'destination': 'Tehran', 'cargo_type': 'Textiles', 'message': 'Two trucks per month'}


class ContentTests(TestCase):
    def test_seeded_company_facts(self):
        c = CompanyInfo.load()
        self.assertEqual(c.email, 'tfahimi54@gmail.com')
        self.assertEqual(c.office_phone, '02188935889')
        self.assertEqual(c.mobile, '09144918300')
        self.assertEqual(c.office_phone_tel, '+982188935889')
        self.assertEqual(Service.objects.count(), 5)
        self.assertEqual(Route.objects.count(), 5)
        self.assertEqual(FleetVehicle.objects.count(), 4)


class PageTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_persian_pages(self):
        for url in ['/', '/services/', '/services/international-transit/', '/routes/', '/about/', '/contact/']:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
            self.assertContains(resp, '<html lang="fa" dir="rtl"')
        home = self.client.get('/')
        self.assertContains(home, 'سریع، ایمن و مطمئن')
        self.assertContains(home, 'درخواست مشاوره حمل')
        self.assertContains(home, 'tfahimi54@gmail.com')
        self.assertContains(home, 'tel:+982188935889')
        self.assertContains(home, 'tel:+989144918300')

    def test_english_pages_and_language_switch(self):
        resp = self.client.get('/en/routes/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<html lang="en" dir="ltr"')
        self.assertContains(resp, 'Iran')
        # the switcher points to the same page in the other language
        self.assertContains(resp, 'href="/routes/" lang="fa"')
        self.assertContains(self.client.get('/routes/'), 'href="/en/routes/" lang="en"')

    def test_turkish_pages(self):
        for url in ['/tr/', '/tr/services/', '/tr/services/international-transit/', '/tr/routes/', '/tr/about/',
                    '/tr/contact/']:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
            self.assertContains(resp, '<html lang="tr" dir="ltr"')
        home = self.client.get('/tr/')
        self.assertContains(home, 'hızlı, güvenli ve güvenilir')
        self.assertContains(home, 'Uluslararası Karayolu Taşımacılığı')     # model content in Turkish
        self.assertContains(home, 'Culfa')
        self.assertContains(home, 'hreflang="tr"')
        self.assertContains(self.client.get('/routes/'), 'href="/tr/routes/" lang="tr"')

    def test_designer_credit_in_footer(self):
        for url in ['/', '/en/', '/tr/']:
            self.assertContains(self.client.get(url), 'images/designer-logo.png')

    def test_seo_tags(self):
        resp = self.client.get('/en/')
        for needle in ['<link rel="canonical" href="http://127.0.0.1:8000/en/">',
                       'hreflang="fa" href="http://127.0.0.1:8000/"', 'hreflang="x-default"',
                       'property="og:title"', 'name="twitter:card"', '"@type": "Organization"']:
            self.assertContains(resp, needle)

    def test_robots_and_sitemap(self):
        self.assertContains(self.client.get('/robots.txt'), 'Sitemap: http://127.0.0.1:8000/sitemap.xml')
        sitemap = self.client.get('/sitemap.xml')
        self.assertContains(sitemap, '/en/services/freight-forwarding/')
        self.assertContains(sitemap, 'hreflang="fa"')

    def test_unknown_service_is_404(self):
        self.assertEqual(self.client.get('/services/nope/').status_code, 404)

    def test_no_invented_facts(self):
        html = self.client.get('/en/').content.decode()
        for forbidden in ['ISO', 'founded in', 'testimonial', '+ shipments', 'years of experience in 20']:
            self.assertNotIn(forbidden, html)


@override_settings(CONTACT_NOTIFY_EMAILS=['ops@example.com'])
class ContactTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = '/contact/'

    def test_valid_request_is_saved_and_emailed(self):
        resp = self.client.post(self.url, VALID, follow=True)
        self.assertEqual(resp.status_code, 200)
        obj = ContactRequest.objects.get()
        self.assertEqual(obj.phone, '09123456789')          # Persian digits normalised
        self.assertEqual(obj.language, 'fa')
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(resp, 'درخواست‌تان ثبت شد')

    def test_json_validation_errors(self):
        resp = self.client.post('/en' + self.url, {'full_name': '', 'phone': 'abc'}, HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data['ok'])
        self.assertIn('full_name', data['errors'])
        self.assertIn('phone', data['errors'])
        self.assertEqual(ContactRequest.objects.count(), 0)

    def test_server_side_validation_without_js(self):
        resp = self.client.post(self.url, {'full_name': 'A', 'phone': ''})
        self.assertEqual(resp.status_code, 400)
        self.assertContains(resp, 'has-error', status_code=400)
        self.assertContains(resp, 'aria-invalid="true"', status_code=400)

    def test_honeypot(self):
        resp = self.client.post(self.url, {**VALID, 'website': 'http://spam'}, HTTP_ACCEPT='application/json')
        self.assertTrue(resp.json()['ok'])
        self.assertEqual(ContactRequest.objects.count(), 0)

    @override_settings(CONTACT_RATE_LIMIT=2)
    def test_rate_limit(self):
        for _ in range(2):
            self.client.post(self.url, VALID, HTTP_ACCEPT='application/json')
        resp = self.client.post(self.url, VALID, HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 429)

    def test_csrf_is_enforced(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.url, VALID).status_code, 403)
        page = client.get(self.url)
        token = page.cookies['csrftoken'].value
        resp = client.post(self.url, {**VALID, 'csrfmiddlewaretoken': token})
        self.assertEqual(resp.status_code, 302)
