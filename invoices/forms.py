from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, MultiField, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import StrictButton
from django.utils.translation import gettext_lazy as _
from invoices.models import Invoice, InvoiceItem, next_invoice_number

DELETION_FIELD_NAME = "DELETE"

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_issue_date'].widget = forms.widgets.DateInput(
                                                                            attrs={
                                                                                'type': 'date', 'placeholder': 'mm/dd/yyyy',
                                                                                })
        self.fields['invoice_status'].widget = forms.HiddenInput()
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML("<div class='row'>\
                    <h3 class='col'>{{ title }} Form</h3>\
                    <div class='col d-flex flex-row-reverse mt-2'>\
                        <div class='btn-group btn-group-sm'>\
                            <button class='btn btn-success' type='submit'><i class='fa fa-check'></i> Save</button>\
                            <button type='button' onclick='window.history.back()' class='btn btn-danger'><i class='fa fa-times'></i> Cancel</button>\
                        </div>\
                    </div>\
                  </div>\
                  <hr>"),
            Div(
                Div(
                    Div(
                        Div(
                            FloatingField(
                                'client_id', 
                                hx_get=reverse_lazy('clients:address'), 
                                hx_target='#id_client_address',
                                hx_trigger='load, change'
                            ),
                            HTML("<div class='form-floating'>\
                                    <textarea class='form-control' placeholder='Address' id='id_client_address' style='height:150px'></textarea>\
                                    <label for='id_client_address'>Address</label>\
                                  </div>"
                            ),
                            css_class="card-body"
                        ),
                        css_class="card"
                    ),
                    css_class="col-sm-6"
                ),
                Div(
                    css_class="col-sm-3"
                ),
                Div(
                    Div(
                        Div(
                            FloatingField(
                                'invoice_status', 
                                type="hidden"
                            ),
                            FloatingField(
                                'invoice_issue_date'
                            ),
                            FloatingField(
                                'invoice_number'
                            ),
                            FloatingField(
                                'invoice_total'
                            ),
                            css_class="card-body"
                        ),
                        css_class="card"
                    ),
                    css_class="col-sm-3"
                ),
                css_class="row"
            ),
            Div(
                style="margin-top: 1rem;",
                css_class="row"
            ),
            Div(
                Div(
                    Div(
                        Div(
                            HTML(
                                "{% load crispy_forms_tags %}{% crispy invoice_item invoice_item_formset %}"
                            ),
                            css_class="card-body"
                        ),
                        css_class="card"
                    ),
                    css_class="col-sm-12"
                ),
                css_class="row"
            ),
            Div(
                Div(
                            Div(
                                HTML("<input type='number' step='1' class='form-control mt-3' id='rowCount' placeholder=''>"),
                                StrictButton(
                                    "Add row",
                                    css_id = "addRowButton",
                                    css_class = "btn btn-primary mt-3"
                                ),
                                css_class="input-group mb-3"
                            ),
                    css_class="col-sm-2"
                ),
                css_class="row"
            ),
        )
        
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        # fields = "__all__"
        exclude = ("item_order",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_description'].widget = forms.widgets.Textarea(attrs={'rows': 2, 'cols': 40})
        
            
    def clean(self):
        cleaned_data = super().clean()
        item_description = cleaned_data.get('item_description')
        item_quantity = cleaned_data.get('item_quantity')
        item_price = cleaned_data.get('item_price')

        if item_quantity and item_quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")

        if item_price and item_price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        
        if not item_description:
            raise forms.ValidationError("Item description cannot be blank.")

        if item_quantity is None:
            raise forms.ValidationError("Item quantity cannot be blank.")

        if item_price is None:
            raise forms.ValidationError("Item price cannot be blank.")

        print("Cleaned Data:", cleaned_data)
        return cleaned_data
    
class InvoiceItemInlineFormset(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        initial_form_count = self.initial_form_count()
        if self.can_delete and (
            self.can_delete_extra or (index is not None and index < initial_form_count)
        ):
            if not form.instance.pk:
                # If the form instance does not exist in the database yet (blank), hide the deletion checkbox
                form.fields[DELETION_FIELD_NAME].widget.attrs['style'] = 'display:none;'
                form.fields[DELETION_FIELD_NAME].widget.attrs['class'] = 'newentry'
            else:
                form.fields[DELETION_FIELD_NAME] = forms.BooleanField(
                    label=_("Delete"),
                    required=False,
                    widget=forms.CheckboxInput(attrs={"class": "mx-3"}),
                )
        
InvoiceItemFormSet = forms.models.inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, formset=InvoiceItemInlineFormset, extra=2, can_delete=True, can_delete_extra=True)

class InvoiceItemFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_tag = False
        self.form_show_labels = False
        self.template = 'table_inline_formset.html'