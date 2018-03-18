from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Order, OrderCSV, Product, Client
from ..accounts.models import Store, Courier, Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('text', 'url','id')


class StoreSerialiser(serializers.ModelSerializer):
    links = LinkSerializer(many=True, required=False, partial=True)

    class Meta:
        model = Store
        fields = ('name', 'members', 'orders', 'color_menu',
                  'company_name', 'url', 'tracking_url',
                  'logo', 'category', 'couriers', 'language',
                  'color_text', 'font', 'color_call_to_action',
                  'allignment', 'size', 'address_line',
                  'zip_code', 'city', 'country', 'links')

    # Store creation is accessible only via admin ( if needed add create function)

    def update(self, instance, validated_data):
        print ("****************** validate data ********")
        print (validated_data)
        print ("*****************************************")
        if 'links' in validated_data:
            links_data = validated_data.pop('links')

        for link_data in links_data:
            try:
                print "**************** testing if Link exists ***********************"
                link = Link.objects.get(url=link_data['url'])
            except ObjectDoesNotExist:
                print "**************** creating object link ***********************"
                link = Link.objects.create(**link_data)
            link.text = link_data.get('text', link.name)
            link.url = link_data.get('url', link.url)
            link.save()
            link.orders.add(instance)
        # If needed add couriers update process

        instance.name = validated_data.get('name', instance.name)
        instance.color_menu = validated_data.get('color_menu', instance.color_menu)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.url = validated_data.get('url', instance.url)
        instance.tracking_url = validated_data.get('tracking_url', instance.tracking_url)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.category = validated_data.get('category', instance.category)
        instance.language = validated_data.get('language', instance.language)
        instance.color_text = validated_data.get('color_text', instance.color_text)
        instance.font = validated_data.get('font', instance.font)
        instance.color_call_to_action = validated_data.get('color_call_to_action', instance.color_call_to_action)
        instance.allignment = validated_data.get('allignment', instance.allignment)
        instance.size = validated_data.get('size', instance.size)
        instance.address_line = validated_data.get('address_line', instance.address_line)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance


class ProductSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('sku', 'name', 'url', 'url_image')
        extra_kwargs = {
            'sku': {
                'validators': []
            }
        }


class ClientSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'email', 'ip_address', 'first_name', 'last_name', 'phone', 'address_line', 'zip_code', 'city', 'country')
        extra_kwargs = {
            'email': {
                'validators': []
            },
            'phone': {
                'validators': []
            }
        }


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    client = ClientSerialiser(partial=True)
    products = ProductSerialiser(many=True, required=False, partial=True)

    class Meta:
        model = Order
        fields = (
            'id', 'store', 'tracking_id', 'file_csv', 'client', 'status', 'origin', 'destination', 'courier', 'owner',
            'date_estimation', 'rate', 'note', 'date_created', 'reason', 'products', 'accept_test_flag')

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        try:
            print "**************** client exists ***********************"
            client_instance = Client.objects.get(email=client_data['email'])
        except ObjectDoesNotExist:
            print "**************** creating a client    ***********************"
            client_instance = Client.objects.create(**client_data)
        if 'products' in validated_data:
            products_data = validated_data.pop('products')
            order_instance = Order.objects.create(client=client_instance, **validated_data)
            for product_data in products_data:
                try:
                    print "**************** Product exists ***********************"
                    product = Product.objects.get(sku=product_data['sku'])
                except ObjectDoesNotExist:
                    print "**************** creating object product ***********************"
                    product = Product.objects.create(**product_data)
                product.orders.add(order_instance)
            return order_instance

        order_instance = Order.objects.create(client=client_instance, **validated_data)
        return order_instance

    def update(self, instance, validated_data):
        print ("****************** validate data ********")
        print (validated_data)
        print ("*****************************************")
        if 'products' in validated_data:
            products_data = validated_data.pop('products')

        if 'client' in validated_data:
            client_data = validated_data.pop('client')
            test_client = True
            print "**************** testing if client mail is correct ***********************"
            if 'email' in client_data:
                if client_data['email'] != instance.client.email:
                    test_client = False
                    print ("****** not updating th client, mail does not match the client")
            if test_client:
                instance.client.ip_address = client_data.get('ip_address', instance.client.ip_address)
                instance.client.first_name = client_data.get('first_name', instance.client.first_name)
                instance.client.last_name = client_data.get('last_name', instance.client.last_name)
                instance.client.phone = client_data.get('phone', instance.client.phone)
                instance.client.address_line = client_data.get('address_line', instance.client.address_line)
                instance.client.zip_code = client_data.get('zip_code', instance.client.zip_code)
                instance.client.country = client_data.get('country', instance.client.country)
                instance.client.city = client_data.get('city', instance.client.city)
                instance.client.save()

        for product_data in products_data:
            try:
                print "**************** testing if product exists ***********************"
                product = Product.objects.get(sku=product_data['sku'])
            except ObjectDoesNotExist:
                print "**************** creating object product ***********************"
                product = Product.objects.create(**product_data)
            product.name = product_data.get('name', product.name)
            product.url = product_data.get('url', product.url)
            product.url_image = product_data.get('url_image', product.url_image)
            product.save()
            product.orders.add(instance)

        instance.tracking_id = validated_data.get('tracking_id', instance.tracking_id)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.courier = validated_data.get('courier', instance.courier)
        instance.status = validated_data.get('status', instance.status)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.note = validated_data.get('note', instance.note)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.accept_test_flag = validated_data.get('accept_test_flag', instance.accept_test_flag)
        instance.save()

        return instance


        # def validate(self, data):
        #     print "************************ Test Validation ************************"
        #     data = super(OrderSerializer, self).validate(data)
        #
        #     try:
        #         data['client'] = Client.objects.get(email=data['client']['email'])
        #     except Client.DoesNotExist:
        #         data['client'] = Client.objects.create(**data['client'])
        #     products=[]
        #     for product in data['products']:
        #         try:
        #             product_instance = Product.objects.get(sku=product['sku'])
        #         except Client.DoesNotExist:
        #             product_instance = Product.objects.create(**product)
        #         products.append(product_instance)
        #     data['products']=products


class OrderCSVSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderCSV
        fields = ('file_csv',)


class CourierSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('text', 'code')
