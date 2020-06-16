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
      image_name: "",
      _type:"",
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
    let url = "http://127.0.0.1:8020/api/task-list/";
    await axios.get(url).then((data) => {
      console.log("backserver data : " + data);
      this.setState({
        take: data,
      });
    });
    
    console.log("whattheFuck:" ,this.state.take);
  };

  handleBackSubmit = async (event) => {
    event.preventDefault();
    const form_data = new FormData();
    form_data.append("title", event.target.content.value);
    console.log("submit:" + event.target.content.value)
    if(event.target.content.value.substring(0,9) == "@startuml") {
      form_data.append("_type", "1");  // plantUML to image
      form_data.append("image_name", this.state.images )
      console.log("12345678910")
    } else {
      form_data.append("_type", "0");  // natural Language to image
    }

    var url = "http://127.0.0.1:8020/api/task-create/";
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
            <Form style={{ align: "middle", justify: "center", }}>
              <Form.Item>
                <textArea
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
            {
                    take.data ? (
                      
                      this.state.images = take.data[0].image_name
                    ) : (
                        null
                      )
            }
            <Form style={{ align: "middle", justify: "center", }}>
              <Form.Item>
                <Title style={{ color: "#00008B" }}>plantUML</Title>
                <textArea
                  name="content"
                  style={{
                    marginLeft: "10px",
                    minHeight: "40vh",
                    minWidth: "45vh",
                  }}
                  
                >
                  {
                    take.data ? (
                      take.data[0].title
                      
                    ) : (
                        null
                      )
                  }
                  
                </textArea>
              </Form.Item>
              <Button
                style={{ marginRight: "10px", marginBottom: "10px" }}
                type="primary"
                htmlType="submit"
              >
                convert from plantUML
              </Button>
            </Form>
            
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
              <Paragraph
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "column",
                  marginTop: "10px",
                  border: "3px solid #6495ED",

                }}
              >
                {take.data ? (
                  <Image
                    src={"http://127.0.0.1:8020" + take.data[0].images + "/?time=" + new Date()}
                    style={{ width: "500px" }}
                    key={take.data[0].id}
                  />
                ) : (
                    <h>when null</h>
                  )}
                {}
              </Paragraph>
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