from django.db import models


class Comparison(models.Model):
    """A Comparison is a collection of diffs, for example as generated and
        exported by the bassist."""
    diffs = models.ManyToManyField("Diff")


class Diff(models.Model):
    # Hashed so it can't get added twice
    content = models.CharField(max_length=250)
    system = models.CharField(max_length=250)
    action = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return "%s|%s|%s" % (self.action, self.system, self.name)


class Set(models.Model):
    """A Set is one or more diffs from a Comparison object. Diffs result from a
        change made to an OS. For example: installing a package."""
    comparison = models.ForeignKey("Comparison")
    diffs = models.ManyToManyField("Diff")


class Playbook(models.Model):
    pass
