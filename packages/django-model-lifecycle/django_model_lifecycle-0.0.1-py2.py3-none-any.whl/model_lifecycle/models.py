from django.db import models


def get_default_lifecycle_state():
    """ get a default value for confirmation status; create new state if not available """
    return LifecycleState.objects.get_or_create(name='pending')[0].id


def get_default_lifecycle_result():
    """ get a default value for confirmation result; create new result if not available """
    return LifecycleResult.objects.get_or_create(name='unknown')[0].id


class ReferenceTable(models.Model):
    """ abstract model for enum-based 'lookup' tables """
    name = models.CharField(max_length=64, blank=True, null=True, help_text='human readable representation of value')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='description of this entry')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class LifecycleState(ReferenceTable):
    """
    Values to reflect the operational activity of a stage.

    default states:
        - pending   = activity on this stage is expected but has not yet started
        - started   = activity on this stage has started
        - completed = activity on this stage has completed
    """


class LifecycleResult(ReferenceTable):
    """
    Values to reflect the outcome of a stage.

    default results:
        - success = stage completed successfully with no issues
        - fail    = stage completed with a well-defined failure condition
        - error   = stage encountered an error and could not complete
        - unknown = stage has not completed, or completion can not be determined
    """


class Lifecycle(models.Model):
    """ individual instance of a model_lifecycle entry """
    is_complete = models.BooleanField(default=False, help_text='set to true when all stages are complete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_stages(self) -> models.query.QuerySet:
        """ get all the stages of this model_lifecycle """
        return self.lifecyclestage_set.all()

    def get_completion_percentage(self) -> float:
        """ get the current completion, as a percentage, of this model_lifecycle """
        return self.lifecyclestage_set.filter(state__name='completed').count() / self.lifecyclestage_set.count()

    def get_current_stage(self):
        """ get the current stage of this model_lifecycle """
        pass

    def get_completed_stages(self) -> models.query.QuerySet:
        """ get completed stages of this model_lifecycle """
        return self.lifecyclestage_set.filter(state__name='completed')

    def get_remaining_stages(self) -> models.query.QuerySet:
        """ get remaining (non-completed) stages of this model_lifecycle """
        return self.lifecyclestage_set.exclude(state__name='completed')

    def add_stage(self, name: str, description: str = None, blocking: bool = None):
        """ add a stage to this model_lifecycle
        Parameters:
            name        - (str) name of this stage
            description - (str) description of this stage
            blocking    - (bool) set this stage to blocking
        """
        data = dict(lifecycle=self, name=name)
        if description:
            data['description'] = description
        if blocking:
            data['blocking'] = blocking
        LifecycleStage.objects.create(**data)

    def add_stages(self, stage_list: list):
        """ add all the stages passed as a list of dictionaries such as:
        [{'name': ''},
        ]
        """
        pass

    @property
    def stages(self):
        return self.get_stages()


class LifecycleStage(models.Model):
    """ individual stage(s) for a model_lifecycle item; identifies where in the overall model_lifecycle a thing is; includes a
    state and a result """
    lifecycle = models.ForeignKey(Lifecycle, on_delete=models.CASCADE, help_text='model_lifecycle this stage belongs to')
    name = models.CharField(max_length=64, unique=True, help_text='short reference for stage')
    description = models.CharField(max_length=255, blank=True, null=True, help_text='detailed description of stage')
    order = models.IntegerField(help_text='operational order of stage (where 1 is the first)')
    state = models.ForeignKey(LifecycleState, default=get_default_lifecycle_state, on_delete=models.CASCADE,
                              help_text='current activity of model_lifecycle stage')
    result = models.ForeignKey(LifecycleResult, default=get_default_lifecycle_result, on_delete=models.CASCADE,
                               help_text='outcome of model_lifecycle stage')
    details = models.CharField(max_length=255, blank=True, null=True,
                               help_text='additional details, such as incomplete reason')
    blocking = models.BooleanField(default=True,
                                   help_text='if True, do not continue to next stage if a failure or error occurs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def update_lifecycle(self):
        """ when this stage is updated (state or result) update the parent LifeCycle accordingly """
        pass

    def save(self, *args, **kwargs):
        if not self.pk and not self.order:
            stage_count = self.lifecycle.lifecyclestage_set.count()
            self.order = stage_count + 1
        super(LifecycleStage, self).save(*args, **kwargs)


class LifecycleField(models.ForeignKey):
    description = 'A field to track the model_lifecycle of a given object entry'

    def __init__(self, **kwargs):
        kwargs['to'] = 'model_lifecycle.Lifecycle'
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['on_delete'] = models.CASCADE
        kwargs['default'] = Lifecycle.objects.create()
        super(LifecycleField, self).__init__(**kwargs)
