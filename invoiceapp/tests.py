from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):

    def setUp(self):
        self.invoice_data = {'date': '2023-10-05', 'customer_name': 'John Doe'}
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_detail_data = {
            'invoice': self.invoice.id,
            'description': 'Product A',
            'quantity': 2,
            'unit_price': 10.00,
            'price': 20.00,
        }
        self.invoice_detail = InvoiceDetail.objects.create(**self.invoice_detail_data)

    def test_create_invoice(self):
        response = self.client.post('/invoices/', self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)  # assuming there's one existing invoice

    def test_get_invoice_list(self):
        response = self.client.get('/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail(self):
        response = self.client.get(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice(self):
        updated_data = {'date': '2023-11-01', 'customer_name': 'Updated Customer'}
        response = self.client.put(f'/invoices/{self.invoice.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, 'Updated Customer')

    def test_delete_invoice(self):
        response = self.client.delete(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_create_invoice_detail(self):
        response = self.client.post('/invoice-details/', self.invoice_detail_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)  # assuming there's one existing detail

    def test_get_invoice_detail_list(self):
        response = self.client.get('/invoice-details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail_detail(self):
        response = self.client.get(f'/invoice-details/{self.invoice_detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice_detail(self):
        updated_data = {'description': 'Updated Product'}
        response = self.client.put(f'/invoice-details/{self.invoice_detail.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InvoiceDetail.objects.get(id=self.invoice_detail.id).description, 'Updated Product')

    def test_delete_invoice_detail(self):
        response = self.client.delete(f'/invoice-details/{self.invoice_detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
