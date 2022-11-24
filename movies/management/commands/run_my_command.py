# This module is used for storing customized management commands

from django.core.management.base import CommandError, BaseCommand  # imported from adding customized commands
from django.utils import timezone
from movies.models import Movie
import logging

logger = logging.getLogger('movies')  # passed name of the loger ('django')


class Command(BaseCommand):
    @staticmethod
    def valid_date(value):
        try:
            return timezone.datetime.strptime(value, '%Y-%m-%d').date()
        except:
            raise CommandError(f'{value} is not a correct date')

    def add_arguments(self, parser):
        parser.add_argument('--start_date', default=timezone.now().date() - timezone.timedelta(days=30),
                            type=self.valid_date)
        parser.add_argument('--end_date', default=timezone.now().date(),
                            type=self.valid_date)

    def handle(self, *args, **options):
        logger.info('Command is starting...')

        start_date = options['start_date']
        end_date = options['end_date']

        logger.info('Updating movies...')
        qs = Movie.objects.filter(release_date__gte=start_date, release_date__lte=end_date)
        cnt = qs.update(is_valid=False)  # cnt is number of movies

        logger.info(f'{cnt} movies updated')
