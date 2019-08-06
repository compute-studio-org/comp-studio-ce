import { Modal, Button } from "react-bootstrap";
import React from "react";
import ReactLoading from "react-loading";

export class ValidatingModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      show: true,
      setShow: true
    };
    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
  }

  handleClose() {
    this.setState({ setShow: false, show: false });
  }
  handleShow() {
    this.setState({ setShow: true, show: true });
  }

  render() {
    return (
      <div>
        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Validating inputs...</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="d-flex justify-content-center">
              <ReactLoading type="spokes" color="#28a745" />
            </div>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}

export const RunModal = ({ handleSubmit }) => {
  const [show, setShow] = React.useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleCloseWithSubmit = () => {
    setShow(false);
    handleSubmit();
  };
  return (
    <>
      <div className="card card-body card-outer">
        <Button
          variant="primary"
          onClick={handleShow}
          className="btn btn-block btn-success"
        >
          <b>Run</b>
        </Button>
      </div>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>
            Are you sure that you want to run this simulation?
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>All sims are sponsored on the development site.</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button
            variant="success"
            onClick={handleCloseWithSubmit}
            type="submit"
          >
            Run simulation
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export const AuthModal = () => {
  const [show, setShow] = React.useState(true);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleCloseWithRedirect = (e, redirectLink) => {
    e.preventDefault();
    setShow(false);
    window.location.replace(redirectLink);
  };
  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Sign up</Modal.Title>
        </Modal.Header>
        <Modal.Body>You must be logged in to run simulations.</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button
            variant="secondary"
            onClick={e => handleCloseWithRedirect(e, "/users/login")}
          >
            <b>Log in</b>
          </Button>
          <Button
            variant="success"
            onClick={e => handleCloseWithRedirect(e, "/users/signup")}
          >
            <b>Sign up</b>
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};
