from django import forms
from .models import Directories


class AddDirectoryForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    # date_added = forms.DateTimeField('date added')
    edit_id = forms.IntegerField(initial=0, widget=forms.HiddenInput())
    name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)
    backup_type = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)
    path = forms.CharField(max_length=200)
    remote_url = forms.GenericIPAddressField(max_length=200, required=False)
    remote_port = forms.IntegerField(initial=22)
    remote_user = forms.CharField(max_length=100, required=False)
    remote_pass = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(render_value=True))
    exclude_dirs = forms.CharField(max_length=5000, widget=forms.Textarea, required=False)

    def __init__(self, item_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if item_id is not None:
            db_dir = Directories.objects.filter(id=item_id)
            if len(db_dir) >= 1:
                db_dir = db_dir[0]
                self.fields['edit_id'].initial = item_id
                self.fields['name'].initial = db_dir.name
                self.fields['location'].initial = db_dir.location
                self.fields['path'].initial = db_dir.path
                self.fields['remote_url'].initial = db_dir.remote_url
                self.fields['remote_port'].initial = db_dir.remote_port
                self.fields['remote_user'].initial = db_dir.remote_user
                self.fields['remote_pass'].initial = db_dir.remote_pass
                excluded = '\r\n'.join(db_dir.exclude_dirs.split(','))
                self.fields['exclude_dirs'].initial = excluded
