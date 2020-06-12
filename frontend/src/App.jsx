import "./App.css";
import React from "react";

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
    if (nextState !== this.state) return true;
    else return false;
  }

  callBackServer = () => {
    fetch("http://127.0.0.1:8020/api/task-list/")
      .then((response) => response.json())
      .then((data) =>
        this.setState({
          take: data,
        })
      );
  };

  handleBackSubmit(event) {
    var url = "http://127.0.0.1:8020/api/task-create/";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(event.target.content.value),
    })
      .then((response) => {
        this.setState({
          take: response,
        });
      })
      .catch(function (error) {
        console.log("ERROR:", error);
      });
    console.log(this.state.take);
  }

  handleSubmit = (e) => {
    console.log("entered handlesubmit");
    console.log(e.target.content.value);
    this.handleBackSubmit(e);
  };

  render() {
    var tasks = this.state.take;
    return (
      <div onSubmitCapture={(e) => this.handleSubmit(e)}>
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
              <div>
                {tasks.map(function (task, index) {
                  return (
                    <div key={index}>
                      <Image
                        src={"http://127.0.0.1:8020" + task.images}
                        style={{ width: "500px" }}
                      ></Image>
                    </div>
                  );
                })}
              </div>
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
