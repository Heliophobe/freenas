# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 21:41


import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import freenasUI.freeadmin.models.fields
import freenasUI.system.models
from freenasUI import choices


def create_system(apps, schema_editor):
    apps.get_model('system', 'Advanced').objects.create()
    apps.get_model('system', 'Settings').objects.create()
    apps.get_model('system', 'Email').objects.create()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advanced',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adv_consolemenu', models.BooleanField(default=False, verbose_name='Enable Console Menu')),
                ('adv_serialconsole', models.BooleanField(default=False, verbose_name='Use Serial Console')),
                ('adv_serialport', models.CharField(choices=[('0x3f8', '0x3f8')], default='0x2f8', help_text='Set this to match your serial port address (0x3f8, 0x2f8, etc.)', max_length=120, verbose_name='Serial Port Address')),
                ('adv_serialspeed', models.CharField(choices=[('9600', '9600'), ('19200', '19200'), ('38400', '38400'), ('57600', '57600'), ('115200', '115200')], default='9600', help_text='Set this to match your serial port speed', max_length=120, verbose_name='Serial Port Speed')),
                ('adv_consolescreensaver', models.BooleanField(default=False, verbose_name='Enable screen saver')),
                ('adv_powerdaemon', models.BooleanField(default=False, verbose_name='Enable powerd (Power Saving Daemon)')),
                ('adv_swapondrive', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Swap size on each drive in GiB, affects new disks only. Setting this to 0 disables swap creation completely (STRONGLY DISCOURAGED).')),
                ('adv_consolemsg', models.BooleanField(default=True, verbose_name='Show console messages in the footer')),
                ('adv_traceback', models.BooleanField(default=True, verbose_name='Show tracebacks in case of fatal errors')),
                ('adv_advancedmode', models.BooleanField(default=False, help_text='By default only essential fields are shown. Fields considered advanced can be displayed through the Advanced Mode button.', verbose_name='Show advanced fields by default')),
                ('adv_autotune', models.BooleanField(default=False, help_text='Attempt to automatically tune the network and ZFS system control variables based on memory available.', verbose_name='Enable autotune')),
                ('adv_debugkernel', models.BooleanField(default=False, help_text='The kernel built with debug symbols will be booted instead.', verbose_name='Enable debug kernel')),
                ('adv_uploadcrash', models.BooleanField(default=True, verbose_name='Enable automatic upload of kernel crash dumps and daily telemetry')),
                ('adv_anonstats', models.BooleanField(default=True, editable=False, verbose_name='Enable report anonymous statistics')),
                ('adv_anonstats_token', models.TextField(blank=True, editable=False)),
                ('adv_motd', models.TextField(default='Welcome', max_length=1024, verbose_name='MOTD banner')),
                ('adv_boot_scrub', models.IntegerField(default=35, editable=False)),
                ('adv_periodic_notifyuser', freenasUI.freeadmin.models.fields.UserField(default='root', help_text='If you wish periodic emails to be sent to a different email address than the alert emails are set to (root) set an email address for a user and select that user in the dropdown.', max_length=120, verbose_name='Periodic Notification User')),
                ('adv_graphite', models.CharField(blank=True, default='', help_text='A hostname or IP here will be used as the destination to send collectd data to using the graphite plugin to collectd.', max_length=120, verbose_name='Remote Graphite Server Hostname')),
                ('adv_fqdn_syslog', models.BooleanField(default=False, verbose_name='Use FQDN for logging')),
            ],
            options={
                'verbose_name': 'Advanced',
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(default='A', max_length=100)),
                ('message_id', models.CharField(max_length=100)),
                ('dismiss', models.BooleanField(default=True)),
                ('timestamp', models.IntegerField(default=freenasUI.system.models.time_now)),
            ],
        ),
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bak_finished', models.BooleanField(default=False, verbose_name='Finished')),
                ('bak_failed', models.BooleanField(default=False, verbose_name='Failed')),
                ('bak_acknowledged', models.BooleanField(default=False, verbose_name='Acknowledged')),
                ('bak_worker_pid', models.IntegerField(null=True, verbose_name='Backup worker PID')),
                ('bak_started_at', models.DateTimeField(verbose_name='Started at')),
                ('bak_finished_at', models.DateTimeField(null=True, verbose_name='Finished at')),
                ('bak_destination', models.CharField(blank=True, max_length=1024, verbose_name='Destination')),
                ('bak_status', models.CharField(blank=True, max_length=1024, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'System Backup',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_type', models.IntegerField()),
                ('cert_name', models.CharField(help_text='Internal identifier of the certificate. Only alphanumeric, "_" and "-" are allowed.', max_length=120, unique=True, verbose_name='Identifier')),
                ('cert_certificate', models.TextField(blank=True, help_text='Cut and paste the contents of your certificate here', null=True, verbose_name='Certificate')),
                ('cert_privatekey', models.TextField(blank=True, help_text='Cut and paste the contents of your private key here', null=True, verbose_name='Private Key')),
                ('cert_CSR', models.TextField(blank=True, help_text='Cut and paste the contents of your CSR here', null=True, verbose_name='Signing Request')),
                ('cert_key_length', models.IntegerField(blank=True, default=2048, null=True, verbose_name='Key length')),
                ('cert_digest_algorithm', models.CharField(blank=True, default='SHA256', max_length=120, null=True, verbose_name='Digest Algorithm')),
                ('cert_lifetime', models.IntegerField(blank=True, default=3650, null=True, verbose_name='Lifetime')),
                ('cert_country', models.CharField(blank=True, help_text='Country Name (2 letter code)', max_length=120, null=True, verbose_name='Country')),
                ('cert_state', models.CharField(blank=True, help_text='State or Province Name (full name)', max_length=120, null=True, verbose_name='State')),
                ('cert_city', models.CharField(blank=True, help_text='Locality Name (eg, city)', max_length=120, null=True, verbose_name='Locality')),
                ('cert_organization', models.CharField(blank=True, help_text='Organization Name (eg, company)', max_length=120, null=True, verbose_name='Organization')),
                ('cert_email', models.CharField(blank=True, help_text='Email Address', max_length=120, null=True, verbose_name='Email Address')),
                ('cert_common', models.CharField(blank=True, help_text='Common Name (eg, FQDN of FreeNAS server or service)', max_length=120, null=True, verbose_name='Common Name')),
                ('cert_serial', models.IntegerField(blank=True, help_text='Serial for next certificate', null=True, verbose_name='Serial')),
                ('cert_chain', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
            },
        ),
        migrations.CreateModel(
            name='CertificateAuthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_type', models.IntegerField()),
                ('cert_name', models.CharField(help_text='Internal identifier of the certificate. Only alphanumeric, "_" and "-" are allowed.', max_length=120, unique=True, verbose_name='Identifier')),
                ('cert_certificate', models.TextField(blank=True, help_text='Cut and paste the contents of your certificate here', null=True, verbose_name='Certificate')),
                ('cert_privatekey', models.TextField(blank=True, help_text='Cut and paste the contents of your private key here', null=True, verbose_name='Private Key')),
                ('cert_CSR', models.TextField(blank=True, help_text='Cut and paste the contents of your CSR here', null=True, verbose_name='Signing Request')),
                ('cert_key_length', models.IntegerField(blank=True, default=2048, null=True, verbose_name='Key length')),
                ('cert_digest_algorithm', models.CharField(blank=True, default='SHA256', max_length=120, null=True, verbose_name='Digest Algorithm')),
                ('cert_lifetime', models.IntegerField(blank=True, default=3650, null=True, verbose_name='Lifetime')),
                ('cert_country', models.CharField(blank=True, help_text='Country Name (2 letter code)', max_length=120, null=True, verbose_name='Country')),
                ('cert_state', models.CharField(blank=True, help_text='State or Province Name (full name)', max_length=120, null=True, verbose_name='State')),
                ('cert_city', models.CharField(blank=True, help_text='Locality Name (eg, city)', max_length=120, null=True, verbose_name='Locality')),
                ('cert_organization', models.CharField(blank=True, help_text='Organization Name (eg, company)', max_length=120, null=True, verbose_name='Organization')),
                ('cert_email', models.CharField(blank=True, help_text='Email Address', max_length=120, null=True, verbose_name='Email Address')),
                ('cert_common', models.CharField(blank=True, help_text='Common Name (eg, FQDN of FreeNAS server or service)', max_length=120, null=True, verbose_name='Common Name')),
                ('cert_serial', models.IntegerField(blank=True, help_text='Serial for next certificate', null=True, verbose_name='Serial')),
                ('cert_chain', models.BooleanField(default=False)),
                ('cert_signedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.CertificateAuthority', verbose_name='Signing Certificate Authority')),
            ],
            options={
                'verbose_name': 'CA',
                'verbose_name_plural': 'CAs',
            },
        ),
        migrations.CreateModel(
            name='CloudCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('provider', models.CharField(choices=[('AMAZON', 'Amazon S3')], max_length=50, verbose_name='Provider')),
                ('attributes', freenasUI.freeadmin.models.fields.DictField(editable=False)),
            ],
            options={
                'verbose_name': 'Cloud Credential',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('em_fromemail', models.CharField(default='', help_text='An email address that the system will use for the sending address for mail it sends, eg: freenas@example.com', max_length=120, verbose_name='From email')),
                ('em_outgoingserver', models.CharField(blank=True, help_text='A hostname or ip that will accept our mail, for instance mail.example.org, or 192.168.1.1', max_length=120, verbose_name='Outgoing mail server')),
                ('em_port', models.IntegerField(default=25, help_text='An integer from 1 - 65535, generally will be 25, 465, or 587', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)], verbose_name='Port to connect to')),
                ('em_security', models.CharField(choices=[('plain', 'Plain'), ('ssl', 'SSL'), ('tls', 'TLS')], default='plain', help_text='encryption of the connection', max_length=120, verbose_name='TLS/SSL')),
                ('em_smtp', models.BooleanField(default=False, verbose_name='Use SMTP Authentication')),
                ('em_user', models.CharField(blank=True, help_text='A username to authenticate to the remote server', max_length=120, null=True, verbose_name='Username')),
                ('em_pass', models.CharField(blank=True, help_text='A password to authenticate to the remote server', max_length=120, null=True, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'Email',
            },
        ),
        migrations.CreateModel(
            name='NTPServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ntp_address', models.CharField(max_length=120, verbose_name='Address')),
                ('ntp_burst', models.BooleanField(default=False, help_text='When the server is reachable, send a burst of eight packets instead of the usual one. This is designed to improve timekeeping quality with the server command and s addresses.', verbose_name='Burst')),
                ('ntp_iburst', models.BooleanField(default=True, help_text='When the server is unreachable, send a burst of eight packets instead of the usual one. This is designed to speed the initial synchronization acquisition with the server command and s addresses.', verbose_name='IBurst')),
                ('ntp_prefer', models.BooleanField(default=False, help_text='Marks the server as preferred. All other things being equal, this host will be chosen for synchronization among a set of correctly operating hosts.', verbose_name='Prefer')),
                ('ntp_minpoll', models.IntegerField(default=6, help_text='The minimum poll interval for NTP messages, as a power of 2 in seconds. Defaults to 6 (64 s), but can be decreased to a lower limit of 4 (16 s)', validators=[django.core.validators.MinValueValidator(4)], verbose_name='Min. Poll')),
                ('ntp_maxpoll', models.IntegerField(default=10, help_text='The maximum poll interval for NTP messages, as a power of 2 in seconds. Defaults to 10 (1,024 s), but can be increased to an upper limit of 17 (36.4 h)', validators=[django.core.validators.MaxValueValidator(17)], verbose_name='Max. Poll')),
            ],
            options={
                'ordering': ['ntp_address'],
                'verbose_name': 'NTP Server',
                'verbose_name_plural': 'NTP Servers',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stg_guiprotocol', models.CharField(choices=[('http', 'HTTP'), ('https', 'HTTPS'), ('httphttps', 'HTTP+HTTPS')], default='http', max_length=120, verbose_name='Protocol')),
                ('stg_guiaddress', models.CharField(blank=True, default='0.0.0.0', max_length=120, verbose_name='WebGUI IPv4 Address')),
                ('stg_guiv6address', models.CharField(blank=True, default='::', max_length=120, verbose_name='WebGUI IPv6 Address')),
                ('stg_guiport', models.IntegerField(default=80, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)], verbose_name='WebGUI HTTP Port')),
                ('stg_guihttpsport', models.IntegerField(default=443, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)], verbose_name='WebGUI HTTPS Port')),
                ('stg_guihttpsredirect', models.BooleanField(default=True, help_text='Redirect HTTP (port 80) to HTTPS when only the HTTPS protocol is enabled', verbose_name='WebGUI HTTP -> HTTPS Redirect')),
                ('stg_language', models.CharField(choices=settings.LANGUAGES, default='en', max_length=120, verbose_name='Language')),
                ('stg_kbdmap', models.CharField(blank=True, choices=choices.KBDMAP_CHOICES(), max_length=120, verbose_name='Console Keyboard Map')),
                ('stg_timezone', models.CharField(choices=choices.TimeZoneChoices(), default='America/Los_Angeles', max_length=120, verbose_name='Timezone')),
                ('stg_sysloglevel', models.CharField(choices=[('f_emerg', 'Emergency'), ('f_alert', 'Alert'), ('f_crit', 'Critical'), ('f_err', 'Error'), ('f_warning', 'Warning'), ('f_notice', 'Notice'), ('f_info', 'Info'), ('f_debug', 'Debug'), ('f_is_debug', 'Is_Debug')], default='f_info', help_text='Specifies which messages will be logged by server. INFO and VERBOSE log transactions that server performs on behalf of the client. f_is_debug specify higher levels of debugging output. The default is f_info.', max_length=120, verbose_name='Syslog level')),
                ('stg_syslogserver', models.CharField(blank=True, default='', help_text='Specifies the server and port syslog messages will be sent to.  The accepted format is hostname:port or ip:port, if :port is not specified it will default to port 514 (this field currently only takes IPv4 addresses)', max_length=120, verbose_name='Syslog server')),
                ('stg_wizardshown', models.BooleanField(default=False, editable=False)),
                ('stg_pwenc_check', models.CharField(editable=False, max_length=100)),
                ('stg_guicertificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Certificate', verbose_name='Certificate')),
            ],
            options={
                'verbose_name': 'General',
            },
        ),
        migrations.CreateModel(
            name='SystemDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_pool', models.CharField(blank=True, max_length=1024, verbose_name='Pool')),
                ('sys_syslog_usedataset', models.BooleanField(default=False, verbose_name='Syslog')),
                ('sys_rrd_usedataset', models.BooleanField(default=True, help_text='Save the Round-Robin Database (RRD) used by system statistics collection daemon into the system dataset', verbose_name='Reporting Database')),
                ('sys_uuid', models.CharField(editable=False, max_length=32)),
                ('sys_uuid_b', models.CharField(blank=True, editable=False, max_length=32, null=True)),
            ],
            options={
                'verbose_name': 'System Dataset',
            },
        ),
        migrations.CreateModel(
            name='Tunable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tun_var', models.CharField(max_length=50, unique=True, verbose_name='Variable')),
                ('tun_value', models.CharField(max_length=512, verbose_name='Value')),
                ('tun_type', models.CharField(choices=[('loader', 'Loader'), ('rc', 'rc.conf'), ('sysctl', 'Sysctl')], default='loader', max_length=20, verbose_name='Type')),
                ('tun_comment', models.CharField(blank=True, max_length=100, verbose_name='Comment')),
                ('tun_enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
            options={
                'ordering': ['tun_var'],
                'verbose_name': 'Tunable',
                'verbose_name_plural': 'Tunables',
            },
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upd_autocheck', models.BooleanField(default=True, verbose_name='Check Automatically For Updates')),
                ('upd_train', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Update',
            },
        ),
        migrations.AddField(
            model_name='certificate',
            name='cert_signedby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.CertificateAuthority', verbose_name='Signing Certificate Authority'),
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.NullBooleanField(default=False, verbose_name='Enable automatic support alerts to iXsystems')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Name of Primary Contact')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Title')),
                ('email', models.EmailField(blank=True, max_length=200, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=200, verbose_name='Phone')),
                ('secondary_name', models.CharField(blank=True, max_length=200, verbose_name='Name of Secondary Contact')),
                ('secondary_title', models.CharField(blank=True, max_length=200, verbose_name='Secondary Title')),
                ('secondary_email', models.EmailField(blank=True, max_length=200, verbose_name='Secondary E-mail')),
                ('secondary_phone', models.CharField(blank=True, max_length=200, verbose_name='Secondary Phone')),
            ],
            options={
                'verbose_name': 'Proactive Support',
            },
        ),
        migrations.AlterUniqueTogether(
            name='alert',
            unique_together=set([('node', 'message_id')]),
        ),
        migrations.RunPython(create_system),
    ]
