import "./App.css";
import React from "react";
import axios from "axios";

import { Image } from "react-bootstrap";
import { Typography, Row, Col, Input, Button, Menu, Form } from "antd";
import logo from "./black_logo.png";
import background from "./Background.jpeg";
import django_logo from "./django.png";
import react_logo from "./react.png";
import { ArrowRightOutlined } from "@ant-design/icons";
const { TextArea } = Input;
const { Title, Paragraph } = Typography;

class App extends React.Component {
  state = {
    take: [],
    check: 0,
    activeItem: {
      id: null,
      title: "",
    },
    description:
      "this is test uml diagram. and you might get also long long descriptions. this is test uml diagram. and you might get also long long descriptions. this is test uml diagram. and you might get also long long descriptions. this is test uml diagram. and you might get also long long descriptions. this is test uml diagram. and you might get also long long descriptions. ",
  };

  shouldComponentUpdate(nextProps, nextState) {
    if (nextState !== this.state) {
      console.log("update entered");
      return true;
    } else return false;
  }

  callBackServer = async () => {
    let url = "http://127.0.0.1:8000/api/task-list/";
    await axios.get(url).then((data) => {
      console.log("backserver data : " + data);
      this.setState({
        take: data,
      });
    });
    // fetch("http://127.0.0.1:8000/api/task-list/")
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log("backresult : " + data);
    //     this.setState({
    //       take: data,
    //     });
    //   });
    console.log(this.state.take);
  };

  handleBackSubmit = async (event) => {
    event.preventDefault();
    const form_data = new FormData();
    form_data.append("title", event.target.content.value);
    // this.setState({
    //   activeItem: {
    //     id: null,
    //     title: event.target.content.value,
    //   },
    // });
    var url = "http://127.0.0.1:8000/api/task-create/";
    await axios
      .post(url, form_data, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        console.log("result : " + res.data);
      })
      .catch((res) => {
        console.log(res);
      });
      this.callBackServer();
  }

  handleSubmit = (e) => {
    console.log("entered handlesubmit");
    console.log(e.target.content.value);
    this.handleBackSubmit(e);
  };

  render() {
    const { take } = this.state;
    console.log(take);
    return (
      <div onSubmitCapture={(e) => this.handleBackSubmit(e)}>
        <Row
          style={{
            backgroundColor: "#F0F8FF",
            minHeight: "5vh",
          }}
        >
          <Image src={logo} style={{ maxHeight: "5vh" }} />
          <Menu
            theme="light"
            mode="horizontal"
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "#F0F8FF",
            }}
          >
            <Menu.Item key="1">Use Case Diagram</Menu.Item>
            <Menu.Item key="2">Class Diagram</Menu.Item>
            <Menu.Item key="3">Sequence Diagram</Menu.Item>
          </Menu>
        </Row>
        <Row
          style={{
            align: "middle",
            justify: "center",
          }}
        >
          <Col
            span={12}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Title style={{ color: "#00008B" }}>Text Input</Title>
            <Form style={{ align: "middle", justify: "center" }}>
              <Form.Item>
                <Input.TextArea
                  name="content"
                  placeholder="Enter a title for your art"
                  style={{
                    marginLeft: "10px",
                    minHeight: "40vh",
                    minWidth: "45vh",
                  }}
                />
              </Form.Item>
              <Button
                style={{ marginRight: "10px", marginBottom: "10px" }}
                type="primary"
                htmlType="submit"
              >
                Convert
              </Button>
            </Form>
            <Typography
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                marginTop: "10px",
                border: "3px solid #6495ED",
              }}
            >
              <Title style={{ color: "#00008B" }}>plantUML</Title>
              <Paragraph>{this.state.description}</Paragraph>
            </Typography>
            <Button style={{ marginTop: "10px", marginBottom: "10px" }}>
              convert from plantUML
            </Button>
          </Col>

          <Col span={12}>
            <div
              style={{
                marginRight: "20px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Title style={{ color: "#00008B" }}>UML Diagram</Title>
              {take.data ? (
                <Image
                  src={"http://127.0.0.1:8000" + take.data[0].images + "/?time=" + new Date()}
                  style={{ width: "500px" }}
                  key={take.data[0].id}
                />
              ) : (
                <h>when null</h>
              )}
              {/* <Image src={"127.0.0.1:8000" + take.data.images} style={{ width: "500px" }} /> */}
              {/* <div>
                {take.map((take, index) => (
                  <div key={index}>
                    <Image
                      src={"http://127.0.0.1:8000" + take.images}
                      style={{ width: "500px" }}
                    ></Image>
                  </div>
                ))}
              </div> */}
            </div>
          </Col>
        </Row>
        <Row
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "#F0F8FF",
            minHeight: "5vh",
          }}
        >
          <h>(C)2020 TTUM. Powered by React</h>
          <Image src={react_logo} style={{ maxHeight: "3vh" }} />
          <h>And Django</h>
          <Image
            src={django_logo}
            style={{ marginLeft: "5px", maxHeight: "3vh" }}
          />
        </Row>
      </div>
    );
  }
}

export default App;