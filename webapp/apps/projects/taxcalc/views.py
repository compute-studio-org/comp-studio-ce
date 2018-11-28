from django.shortcuts import render, redirect
from webapp.apps.core.compute import Compute
from webapp.apps.core.views import CoreRunDetailView, CoreRunDownloadView
from webapp.apps.core.models import Tag, TagOption
from webapp.apps.core.constants import WEBAPP_VERSION
from webapp.apps.core.submit import BadPost, handle_submission
from django.views import View

from .models import TaxcalcRun
from .param_displayer import ParamDisplayer
from .submit import Submit, Save
from .forms import TaxcalcInputsForm
from .meta_parameters import meta_parameters
from .constants import TAXCALC_VERSION
from .constants import (DISTRIBUTION_TOOLTIP, DIFFERENCE_TOOLTIP,
                         PAYROLL_TOOLTIP, INCOME_TOOLTIP, BASE_TOOLTIP,
                         REFORM_TOOLTIP, INCOME_BINS_TOOLTIP,
                         INCOME_DECILES_TOOLTIP, START_YEARS,
                         DATA_SOURCES,
                         TAXCALC_VERSION)


compute = Compute()


def get_version(url_obj, attr_name, current_version):
    """
    get formatted python version of library for diplay on web page
    """
    # need to chop off the commit reference on older runs
    vers_disp = (getattr(url_obj, attr_name)
                 if getattr(url_obj, attr_name) is not None
                 else current_version)
    # only recently start storing webapp version. for older runs display
    # the current version. an alternative is to display the first stable
    # version if url.webapp_version is None
    if len(vers_disp.split('.')) > 3:
        vers_disp = '.'.join(vers_disp.split('.')[:-1])

    return vers_disp


class TaxcalcInputsView(View):
    FormCls = TaxcalcInputsForm
    ParamDisplayerCls = ParamDisplayer
    SubmitCls = Submit
    SaveCls = Save
    result_header = "Tax-Calculator Results"
    template_name = "taxcalc/input_form.html"
    name = "Tax-Calculator"
    app_name = "taxcalc"
    meta_parameters = meta_parameters
    meta_options = {"start_years": START_YEARS, "data_sources": DATA_SOURCES}
    has_errors = False
    upstream_version = TAXCALC_VERSION

    def get(self, request, *args, **kwargs):
        print("method=GET", request.GET)
        inputs_form = self.FormCls(request.GET.dict())
        if inputs_form.is_valid():
            inputs_form.clean()
        else:
            inputs_form = FormCls()
            inputs_form.is_valid()
            inputs_form.clean()
        names = {mp.name for mp in self.meta_parameters.parameters}
        valid_meta_params = {
            k: inputs_form.cleaned_data.get(k, "") for k in names
        }

        pd = self.ParamDisplayerCls(**valid_meta_params)
        metadict = dict(valid_meta_params, **self.meta_options)
        context = dict(
            form=inputs_form,
            default_form=pd.default_form(),
            upstream_version=self.upstream_version,
            webapp_version=WEBAPP_VERSION,
            has_errors=self.has_errors,
            enable_quick_calc=True,
            **metadict
        )
        return render(request, "taxcalc/input_form.html", context)

    def post(self, request, *args, **kwargs):
        print("method=POST get", request.GET)
        print("method=POST post", request.POST)
        result = handle_submission(
            request, compute, self.SubmitCls, self.SaveCls
        )
        # case where validation failed
        if isinstance(result, BadPost):
            return submission.http_response_404

        # No errors--submit to model
        if result.save is not None:
            print("redirecting...", result.save.runmodel.get_absolute_url())
            return redirect(result.save.runmodel)
        # Errors from taxcalc.tbi.reform_warnings_errors
        else:
            inputs_form = result.submit.form
            valid_meta_params = result.submit.valid_meta_params
            has_errors = result.submit.has_errors

        pd = self.ParamDisplayerCls(**valid_meta_params)
        metadict = dict(valid_meta_params, **self.meta_options)
        context = dict(
            form=inputs_form,
            default_form=pd.default_form(),
            upstream_version=self.upstream_version,
            webapp_version=WEBAPP_VERSION,
            has_errors=self.has_errors,
            enable_quick_calc=ENABLE_QUICK_CALC,
            **metadict
        )
        return render(request, "taxcalc/input_form.html", context)

class TaxcalcRunDetailView(CoreRunDetailView):
    model = TaxcalcRun

    result_header = "Static Results"

    tags = [
        Tag(key="table_type",
            values=[
                TagOption(
                    value="dist",
                    title="Distribution Table",
                    tooltip=DISTRIBUTION_TOOLTIP,
                    children=[
                        Tag(key="law",
                            values=[
                                TagOption(
                                    value="current",
                                    title="Current Law",
                                    active=True,
                                    tooltip=BASE_TOOLTIP),
                                TagOption(
                                    value="reform",
                                    title="Reform",
                                    tooltip=REFORM_TOOLTIP)])]),
                TagOption(
                    value="diff",
                    title="Difference Table",
                    tooltip=DIFFERENCE_TOOLTIP,
                    active=True,
                    children=[
                        Tag(key="tax_type",
                            values=[
                                TagOption(
                                    value="payroll",
                                    title="Payroll Tax",
                                    tooltip=PAYROLL_TOOLTIP),
                                TagOption(
                                    value="ind_income",
                                    title="Income Tax",
                                    tooltip=INCOME_TOOLTIP),
                                TagOption(
                                    value="combined",
                                    title="Combined",
                                    active=True,
                                    tooltip="")  # TODO
                            ])])]),
        Tag(key="grouping",
            values=[
                TagOption(
                    value="bins",
                    title="Income Bins",
                    active=True,
                    tooltip=INCOME_BINS_TOOLTIP),
                TagOption(
                    value="deciles",
                    title="Income Deciles",
                    tooltip=INCOME_DECILES_TOOLTIP)
            ])]
    aggr_tags = [
        Tag(key="law",
            values=[
                TagOption(
                    value="current",
                    title="Current Law"),
                TagOption(
                    value="reform",
                    title="Reform"),
                TagOption(
                    value="change",
                    title="Change",
                    active=True)
            ])]

    def has_link_to_dyn(self):
        assumptions = self.object.inputs.upstream_parameters.get('assumption', None)
        if assumptions is None:
            return True
        else:
            return all(len(assumptions[d]) == 0 for d in assumptions)


class TaxcalcRunDownloadView(CoreRunDownloadView):
    model = TaxcalcRun
