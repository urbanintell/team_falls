from django import forms
from django.db import models
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question
from app.data_client import DataClient

def generate_form(field, field_widget = None, field_choices = None):
    if field['type'] == "boolean":
        return forms.BooleanField(
            label = field['content'],
            required = False,
        )
    elif field['type'] == "choice":
        return forms.ChoiceField(
            label = field['content'],
            widget = field_widget,
            choices = field_choices,
            required = False,
        )
    elif field['type'] == "integer":
        return forms.IntegerField(
            label = field['content'],
            required = False,
        )
    elif field['type'] == "char":
        return forms.CharField(
            label = field['content'],
            required = False,
        )

class LoginForm(forms.Form):
    identity = forms.TypedChoiceField(
        label = 'Identify Who you are',
        choices = (('patient', 'Patient'),
                ('care_provider', 'Care Provider')),
        required = True,
    )
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForms'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

class LoginCPForm(forms.Form):
    username = forms.CharField(
        label = "Username:",
        max_length = 80,
        required = True,
    )
    password = forms.CharField(
        label = "Password:",
        widget = forms.PasswordInput,
        max_length = 80,
        required = True,
    )
    def __init__(self, *args, **kwargs):
        super(LoginCPForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginCPForms'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

class SearchPatientForm(forms.Form):
    patient_name = forms.CharField(
        label = "Patient Name:",
        max_length = 80,
        required = True,
    )

    def __init__(self, *args, **kwargs):
        super(SearchPatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-searchPatientForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Search'))

class QuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        CHOICES = ((True, 'Yes',), (False, 'No',))
        for i, question in enumerate(data_client.questions['questions']):
            field_name = "question" + str(i)
            self.fields[field_name] = generate_form(question, forms.RadioSelect, CHOICES)
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

# class TugForm(forms.Form):
#     tg_test_details = forms.MultipleChoiceField(
#         label = '',
#         choices = (
#             ('no_problem', "No Problems"),
#             ('loss_of_balance', 'Loss of Balance'),
#             ('steady_self_on_walls', 'Steadying Self on Walls'),
#             ('shuffling', 'Shuffling'),
#             ('short_stride', 'Short Stride'),
#             ('little_or_no_arm_swing', 'Little or no arm swing'),
#             ('en_bloc_turning', 'En bloc turning'),
#             ('not_using_assitive_device_properly', 'Not using assitive device properly'),
#         ),
#         initial = None,
#         required = False,
#         widget = forms.CheckboxSelectMultiple,
#     )

class AssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assessments_chosen = kwargs.pop('assessments_chosen', None)
        super(AssessmentForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for name in assessments_chosen:
            print (name)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        if assessments_chosen:
            for test in data_client.func_test:
                if test['name'] in assessments_chosen:
                    test_fieldset = Fieldset(test['name'], css_class=test['name'])
                    for i, form in enumerate(test['forms']):
                        field_name = test['name'] + "_form" + str(i)
                        self.fields[field_name] = generate_form(form, None, None)
                        test_fieldset.append(Field(field_name))
                        # self.fields[field_name].widget = forms.HiddenInput()
                    self.helper.layout.append(test_fieldset)
        else:
            for test in data_client.func_test:
                if test['is_recommended']:
                    self.fields[test['name']] = forms.BooleanField(
                        label = test['name'] + " (Recommended)",
                        required = False,
                    )
                else:
                    self.fields[test['name']] = forms.BooleanField(
                        label = test['name'],
                        required = False,
                    )
        self.helper.form_id = 'id-assessmentForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class TugForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TugForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test['name'] == "Timed Up and Go Test":
                tug_test = test
                break
        for i, form in enumerate(tug_test['forms']):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class ThirtySecStandForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ThirtySecStandForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test['name'] == "30-Second Chair Stand":
                thirty_test = test
                break
        for i, form in enumerate(thirty_test['forms']):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class BalanceTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BalanceTestForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test['name'] == "4 Stage Balance Test":
                balance_test = test
                break
        for i, form in enumerate(balance_test['forms']):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class NoteForm(forms.Form):
    note = forms.CharField(
        widget=forms.Textarea,
        label = 'Note:',
        required = False,
    )

class MedicationsForm(forms.Form):
    #hard code medications for now, will generate it dynamically next step
    def __init__(self, *args, **kwargs):
        super(MedicationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    asprin = forms.CharField(
        label = 'Asprin',
        required = False,
    )
    isosorbide = forms.CharField(
        label = 'Isosorbide',
        required = False,
    )

class ProblemsForm(forms.Form):
    problems = forms.CharField(
        label = 'Problems',
        required = False,
    )
    def __init__(self, *args, **kwargs):
        super(ProblemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class MedicationsLinkedForm(forms.Form):
    medicationsLinked = forms.CharField(
        label = 'Medications linked to Falls',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(MedicationsLinkedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-medicationLinkedForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class ExamsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExamsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        self.helper.layout = Layout()
        for exam in data_client.physical_exam:
            exam_fieldset = Fieldset(exam['name'], css_class = exam['name'])
            for i, form in enumerate(exam['forms']):
                field_name = exam['name'] + "_form" + str(i)
                self.fields[field_name] = generate_form(form)
                exam_fieldset.append(Field(field_name))
            self.helper.layout.append(exam_fieldset)
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class ResultsForm(forms.Form):
    """
    This is a generic results form that will show every intervention
    """
    def __init__(self, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        self.helper.layout = Layout()
        for intervention_key, intervention in data_client.intervention_list.items():
            intervention_fieldset = Fieldset(intervention['name'], css_class='field_set_results')
            for i, form in enumerate(intervention['forms']):
                field_name = intervention['name'] + "_form" + str(i)
                self.fields[field_name] = generate_form(form)
                intervention_fieldset.append(Field(field_name))
            self.helper.layout.append(intervention_fieldset)
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Submit'))

class MessageForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
