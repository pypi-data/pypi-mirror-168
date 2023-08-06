from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from common.models import Channel, Language, Classification, Priority, Status
from payment_gateway.models import PaymentCredential
from subscription.models import Subscription
from ticket.models import Filter


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            channels = ["Phone", "Email", "Web", "Facebook", "Twitter", "Chat", "Forum", "Feedback Widget"]
            languages = ["English", "Hindi", "Urdu", "Telugu", "Marathi", "Kannada"]
            classifications = ["Problem", "Feature", "Question", "Others"]
            priorities = ["High", "Low", "Normal"]
            statuses = ["Open", "Closed", "Resolved", "Assigned", "Pending", "Unresolved", "Unassigned", "Overdue"]
            filters = ["Product", "Staff", "Customer", "Period"]
            for channel in channels:
                if not Channel.objects.filter(name=channel).exists():
                    Channel.objects.create(name=channel)
            self.stdout.write("Default channels ................ " + self.style.SUCCESS("OK"))
            for language in languages:
                if not Language.objects.filter(name=language).exists():
                    Language.objects.create(name=language)
            self.stdout.write("Default languages ................ " + self.style.SUCCESS("OK"))
            for classification in classifications:
                if not Classification.objects.filter(name=classification).exists():
                    Classification.objects.create(name=classification)
            self.stdout.write("Default classifications ................ " + self.style.SUCCESS("OK"))
            for priority in priorities:
                if not Priority.objects.filter(name=priority).exists():
                    Priority.objects.create(name=priority)
            self.stdout.write("Default priorities ................ " + self.style.SUCCESS("OK"))
            for status in statuses:
                if not Status.objects.filter(status=status).exists():
                    Status.objects.create(status=status)
            self.stdout.write("Default ticket statuses ................ " + self.style.SUCCESS("OK"))
            for filter_ in filters:
                if not Filter.objects.filter(name=filter_).exists():
                    Filter.objects.create(name=filter_)
            self.stdout.write("Default dashboard filters ................ " + self.style.SUCCESS("OK"))

            # Trial
            modules = ContentType.objects.filter(
                model__in=["ticket", "lead", "contact", "account"]
            ).values_list("id", flat=True)
            subscription, _ = Subscription.objects.get_or_create(
                name="Trial", employees=10,
                max_storage=2, is_trial=True, is_free=True, price=0, interval=15)
            subscription.modules.set(modules)

            # Starter Plan
            modules = ContentType.objects.filter(model__in=["ticket"]).values_list("id", flat=True)
            subscription, _ = Subscription.objects.get_or_create(name="Starter", employees=3,
                                                                 price=50, interval=15,
                                                                 max_storage=1)
            subscription.modules.set(modules)

            # Standard Plan
            modules = ContentType.objects.filter(model__in=["ticket", "lead"]).values_list("id", flat=True)
            subscription, _ = Subscription.objects.get_or_create(name="Standard", employees=7, max_storage=3,
                                                                 is_recommended=True, price=100, interval=30)
            subscription.modules.set(modules)

            # Professional Plan
            starter_modules = ContentType.objects.filter(
                model__in=["ticket", "lead", "account", "contact"]).values_list("id", flat=True)
            subscription, _ = Subscription.objects.get_or_create(name="Professional", employees=15, max_storage=10,
                                                                 price=300, interval=30)
            subscription.modules.set(starter_modules)
            self.stdout.write("Default subscription packages ................ " + self.style.SUCCESS("OK"))

            razorpay_key_id = "rzp_test_FGwu2m3Yd2jJpm"
            razorpay_key_secret = "OwYEBj66uMCFEJlGFj9ntaoj"
            if not PaymentCredential.objects.filter(name="razorpay", public_key=razorpay_key_id,
                                                    secret_key=razorpay_key_secret, organisation=None).exists():
                PaymentCredential.objects.create(name="razorpay", public_key=razorpay_key_id,
                                                 secret_key=razorpay_key_secret, organisation=None, is_default=True)
            self.stdout.write("Default payment credentials ................ " + self.style.SUCCESS("OK"))
            self.stdout.write(
                self.style.SUCCESS(
                    'All default values created successfully.'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    str(error)
                )
            )
