# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间 ')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('count', models.IntegerField(verbose_name='数量', default=1)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')),
                ('comment', models.TextField(verbose_name='评价信息', default='')),
            ],
            options={
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间 ')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(max_length=64, serialize=False, verbose_name='订单号', primary_key=True)),
                ('total_count', models.IntegerField(verbose_name='商品总数', default=1)),
                ('total_amount', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总金额')),
                ('trans_cost', models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')),
                ('pay_method', models.SmallIntegerField(verbose_name='支付方式', choices=[(1, '货到付款'), (2, '支付宝')], default=1)),
                ('status', models.SmallIntegerField(verbose_name='订单状态', choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1)),
                ('trade_id', models.CharField(max_length=100, unique=True, verbose_name='支付编号', null=True, blank=True)),
            ],
            options={
                'db_table': 'df_order_info',
            },
        ),
    ]
