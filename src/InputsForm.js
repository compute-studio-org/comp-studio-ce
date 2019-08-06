"use strict";

import * as yup from "yup";
import React from "react";
import { Formik, Form } from "formik";
import axios from "axios";

import {
  MetaParameters,
  MajorSection,
  LoadingElement,
  Preview,
  SectionHeaderList,
  ErrorCard
} from "./components";
import { ValidatingModal, RunModal, AuthModal } from "./modal";
import { formikToJSON, convertToFormik } from "./ParamTools";

// need to require schema in model_parameters!
const tbLabelSchema = yup.object().shape({
  year: yup.number(),
  MARS: yup.string(),
  idedtype: yup.string(),
  EIC: yup.string(),
  data_source: yup.string()
});

class InputsForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      initialValues: this.props.initialValues,
      sects: false,
      model_parameters: false,
      resetting: false,
      timer: null
    };
    this.resetInitialValues = this.resetInitialValues.bind(this);
    this.poll = this.poll.bind(this);
    this.killTimer = this.killTimer.bind(this);
  }

  componentDidMount() {
    if (this.props.fetchInitialValues) {
      this.props.fetchInitialValues().then(data => {
        const [
          initialValues,
          sects,
          model_parameters,
          meta_parameters,
          schema,
          unknownParams
        ] = convertToFormik(data);
        let hasSimData = !!data.detail && !!data.detail.sim;
        this.setState({
          initialValues: initialValues,
          sects: sects,
          model_parameters: model_parameters,
          meta_parameters: meta_parameters,
          schema: schema,
          extend: "extend" in data ? data.extend : false,
          unknownParams: unknownParams,
          creationDate: hasSimData ? data.detail.sim.creation_date : null,
          modelVersion: hasSimData ? data.detail.sim.model_version : null,
          detailAPIURL: !!data.detail ? data.detail.api_url : null
        });
      });
    }
  }

  resetInitialValues(metaParameters) {
    this.setState({ resetting: true });
    this.props
      .resetInitialValues({ meta_parameters: metaParameters })
      .then(data => {
        const [
          initialValues,
          sects,
          model_parameters,
          meta_parameters,
          schema,
          unknownParams
        ] = convertToFormik(data);
        this.setState({
          initialValues: initialValues,
          sects: sects,
          model_parameters: model_parameters,
          meta_parameters: meta_parameters,
          schema: schema,
          extend: "extend" in data ? data.extend : false,
          resetting: false
        });
      });
  }

  poll(actions, respData) {
    let timer = setInterval(() => {
      axios
        .get(respData.api_url)
        .then(response => {
          if (response.data.status === "SUCCESS") {
            actions.setSubmitting(false);
            actions.setStatus({
              status: response.data.status,
              simUrl: response.data.sim.gui_url
            });
            this.killTimer();
            window.location.replace(response.data.sim.gui_url);
          } else if (response.data.status === "INVALID") {
            actions.setSubmitting(false);
            actions.setStatus({
              status: response.data.status,
              serverErrors: response.data.errors_warnings
            });
            this.killTimer();
          }
        })
        .catch(error => {
          console.log("polling error:");
          console.log(error);
          this.killTimer();
          actions.setSubmitting(false);
          // request likely cancelled because timer was killed.
          console.log("iscancel", axios.isCancel(error));
          if (!axios.isCancel(error)) {
            alert("There was an error validating your inputs.");
          }
        });
    }, 1000);
    this.setState({ timer: timer });
  }

  killTimer() {
    if (!!this.state.timer) {
      clearInterval(this.state.timer);
      this.setState({ timer: null });
    }
  }

  componentWillUnmount() {
    this.killTimer();
  }

  render() {
    if (
      !this.state.model_parameters ||
      !this.state.initialValues ||
      this.state.resetting
    ) {
      return <LoadingElement />;
    }
    console.log("rendering");
    let meta_parameters = this.state.meta_parameters;
    let model_parameters = this.state.model_parameters;
    let initialValues = this.state.initialValues;
    let schema = this.state.schema;
    let sects = this.state.sects;
    let extend = this.state.extend;
    let hasUnknownParams = this.state.unknownParams.length > 0;
    let unknownParamsErrors = { "Unknown Parameters": { errors: {} } };
    if (hasUnknownParams) {
      for (const param of this.state.unknownParams) {
        unknownParamsErrors["Unknown Parameters"].errors[param] =
          "This parameter is no longer used.";
      }
    }
    return (
      <div>
        <Formik
          initialValues={initialValues}
          validationSchema={schema}
          validateOnChange={false}
          validateOnBlur={true}
          enableReinitialize={true}
          onSubmit={(values, actions) => {
            const [meta_parameters, adjustment] = formikToJSON(
              values,
              this.state.schema,
              tbLabelSchema,
              this.state.extend
            );
            console.log("submitting");
            console.log(adjustment);
            console.log(meta_parameters);

            let formdata = new FormData();
            formdata.append("adjustment", JSON.stringify(adjustment));
            formdata.append("meta_parameters", JSON.stringify(meta_parameters));
            formdata.append("client", "web-beta");
            this.props
              .doSubmit(formdata)
              .then(response => {
                console.log("success");
                console.log(response.data.pk);
                actions.setStatus({
                  status: "PENDING",
                  inputs_pk: response.data.pk,
                  api_url: response.data.api_url
                });
                // set submitting as false in poll func.
                this.poll(actions, response.data);
              })
              .catch(error => {
                console.log("error", error);
                if (error.response.status == 403) {
                  actions.setStatus({
                    auth: "You must be logged in to publish a model."
                  });
                }
              });
          }}
          render={({
            handleSubmit,
            handleChange,
            handleBlur,
            status,
            isSubmitting,
            errors,
            values,
            setFieldValue,
            touched
          }) => (
            <Form>
              {isSubmitting ? <ValidatingModal /> : <div />}
              {status && status.auth ? <AuthModal /> : <div />}

              <div className="row">
                <div className="col-sm-4">
                  <ul className="list-unstyled components sticky-top scroll-y">
                    <li>
                      <MetaParameters
                        meta_parameters={meta_parameters}
                        values={values.meta_parameters}
                        touched={touched}
                        resetInitialValues={this.resetInitialValues}
                      />
                    </li>
                    <li>
                      <SectionHeaderList sects={sects} />
                    </li>
                    <li>
                      <RunModal handleSubmit={handleSubmit} />
                    </li>
                  </ul>
                </div>
                <div className="col-sm-8">
                  {status &&
                  status.status === "INVALID" &&
                  status.serverErrors ? (
                    <ErrorCard
                      errorMsg={
                        <p>
                          "Some fields have errors. These must be fixed " +
                          "before the simulation can be submitted."
                        </p>
                      }
                      errors={status.serverErrors}
                      model_parameters={model_parameters}
                    />
                  ) : (
                    <div />
                  )}

                  {hasUnknownParams ? (
                    <ErrorCard
                      errorMsg={
                        <p>
                          {"One or more parameters have been renamed or " +
                            "removed since this simulation was run on " +
                            `${this.state.creationDate} with version ${
                              this.state.modelVersion
                            }. You may view the full simulation detail `}
                          <a href={this.state.detailAPIURL}>here.</a>
                        </p>
                      }
                      errors={unknownParamsErrors}
                      model_parameters={{}}
                    />
                  ) : (
                    <div />
                  )}

                  <Preview
                    values={values}
                    schema={schema}
                    tbLabelSchema={tbLabelSchema}
                    transformfunc={formikToJSON}
                    extend={extend}
                  />
                  {Object.entries(sects).map(function(msect_item, ix) {
                    // msect --> section_1: dict(dict) --> section_2: dict(dict)
                    let msect = msect_item[0];
                    let section_1_dict = msect_item[1];
                    return (
                      <MajorSection
                        key={`${msect}-component`}
                        msect={msect}
                        section_1_dict={section_1_dict}
                        model_parameters={model_parameters}
                        handleSubmit={handleSubmit}
                        handleChange={handleChange}
                        status={status}
                        errors={errors}
                        values={values}
                        setFieldValue={setFieldValue}
                        handleBlur={handleBlur}
                      />
                    );
                  })}
                </div>
              </div>
            </Form>
          )}
        />
      </div>
    );
  }
}

export { InputsForm };
