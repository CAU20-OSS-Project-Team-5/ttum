import "./App.css";
import React from "react";
import axios from "axios";

import { Image } from "react-bootstrap";
import { Typography, Row, Col, Input, Button, Menu, Form } from "antd";
import logo from "./ttum_logo.png";

import django_logo from "./django.png";
import react_logo from "./react.png";
const { TextArea } = Input;
const { Title, Paragraph } = Typography;

class App extends React.Component {
  state = {
    take: [],
    check: 0,
    image: "",
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

  setSState = () => {
    const { take } = this.state;
   
    take.data ? (
      this.setState({
        image: take.data[0].image_name,
      })
    ) : (
      this.setState({image: "0"})  
    )
    console.log(this.state.image)

  }

  callBackServer = async () => {
    let url = "http://127.0.0.1:8020/api/task-list/";
    await axios.get(url).then((data) => {
      console.log("backserver data : " + data);
      this.setState({
        take: data,
        //image: this.state.data.image_name
      });
    });
    
    this.setSState();
  };

  

  handleBackSubmit = async (event) => {
    event.preventDefault();
    const form_data = new FormData();
    form_data.append("title", event.target.content.value);
    console.log("submit:" + event.target.content.value)
    if(event.target.content.value.substring(0,9) == "@startuml") {
      form_data.append("_type", "1");  // plantUML to image
      form_data.append("image_name", this.state.image)
    } else {
      form_data.append("_type", "0");  // natural Language to image
      form_data.append("image_name", "" )
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
          <Image src={logo} style={{ maxHeight: "8vh" }} />
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
            <Form style={{ display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center", }}>
              <Form.Item>
                <textArea
                  name="content"
                  placeholder="Enter sentences, line by line, to create UML image"
                  
                  style={{
                    marginLeft: "10px",
                    minHeight: "40vh",
                    minWidth: "45vh",
                    border: "3px solid #6495ED",
                    width: 500,
                    fontSize: 18,
                    
                  }}
                  
                />
              </Form.Item>
              <Button
                style={{ 
                  marginRight: "10px", 
                  marginBottom: "10px",
                  width: 120,
                  height: 40,
                }}
                type="primary"
                htmlType="submit"
              >
                Convert
              </Button>
            </Form>
           
              
            
            <Title style={{ color: "#00008B" }}>PlantUML Text</Title>
            <Form style={{ display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center", }}>
              <Form.Item>
                
                <textArea
                  name="content"
                  style={{
                    marginLeft: "10px",
                    minHeight: "40vh",
                    minWidth: "45vh",
                    border: "3px solid #6495ED",
                    width: 500,
                    fontSize: 18,
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
                style={{ 
                  marginRight: "10px", 
                  marginBottom: "10px",
                  height: 40, 
                }}
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
                  width: 700,
                  height: 600,
                  border: "3px solid #6495ED",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {take.data ? (
                  <Image
                    src={"http://127.0.0.1:8020" + take.data[0].images + "/?time=" + new Date()}
                    style={{
                      width: 500,
                    }}
                    key={take.data[0].id}
                  />
                ) : (
                    <h></h>
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