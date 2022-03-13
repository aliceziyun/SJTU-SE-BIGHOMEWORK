<template>
    <div>
        <a-row>
            <a-col :span="10">
                <p style="margin-left:370px;margin-top:30px;font-size:30px">个 人</p> 
            </a-col>
            <a-col :span="4">
                <a-avatar :size="100" style="backgroundColor:#000000;" icon="user"/>    <!-- 这里之后需要绑定信息 -->      
            </a-col>
             <a-col :span="10">
                <p style="margin-right:370px;margin-top:30px;font-size:30px">信 息</p> 
            </a-col>
        </a-row>
            <a-card style="background:black;width:1000px;height:500px;margin:20px auto;">
                <a-row>
                    <a-col :span="2">
                        <p style="margin-top:23px">
                            <a-icon slot="prefix" type="user" style="color:white;fontSize:25px"/>
                        </p>
                    </a-col>
                    <a-col :span="2">
                        <p style="fontSize:20px;color:white; margin-top:20px;fontWeight: 500">
                            昵称
                        </p>
                    </a-col>
                </a-row>

                <a-row>
                    <a-col :span="2">
                        <p style="margin-top:23px">
                            <a-icon slot="prefix" type="mail" style="color:white;fontSize:25px"/>
                        </p>
                    </a-col>
                    <a-col :span="2">
                        <p style="fontSize:20px;color:white; margin-top:20px;fontWeight: 500">
                            邮箱
                        </p>
                    </a-col>
                </a-row>

                <a-row>
                    <a-col :span="2">
                        <p style="margin-top:23px">
                            <a-icon slot="prefix" type="solution" style="color:white;fontSize:25px"/>
                        </p>
                    </a-col>
                    <a-col :span="2">
                        <p style="fontSize:20px;color:white; margin-top:20px;fontWeight: 500">
                            简介
                        </p>
                    </a-col>
                </a-row>

                <a-card id="message-card"></a-card>
            </a-card>
            <a-button type="primary" id="change-button">
                <p style="fontSize:15px;fontWeight:500;margin-top:8px;">修改个人信息</p>
            </a-button>
    </div>
</template>

<style scoped>
#message-card{
    border-width:2px;
    border-color:white;
    background:black;
    width:900px;
    height:200px;
    margin:10px auto;
}

#change-button{
    background-color: black;
    border-color: black;
    width: 200px;
    height: 40px;
    margin-top:10px;
    margin-right:10px;
    border-radius:10px;
}

.ant-btn-primary:hover,
.ant-btn-primary:focus{
    background-color: #2F4F4F !important;
}
</style>