<template>
  <div>
    <div class="row">
            <h1>Get Help Here...</h1>
        </div>

        <h3>Edit your files</h3>
        <ul class="help">
        <li>We supprt different formats, sheets, pictures. You can edit files more efficiently with Hotkeys.</li>
        <li>You can make comments in your team files. All of your teammates will recieve comments from newly edited files.</li>
        <li>Afraid of mistaken editing? Use Version Backtracking to recover your previous files.</li>
        <li>Export pdf or word as you like.</li>
        </ul>


        <h3>Manage your team</h3>
        <ul class="help">
        <li>Create new team as team manager.</li>
        <li>Invite members with no limitation.</li>
        </ul>

        <h3>Participate in cooperative project</h3>
        <ul class="help">
        <li>Apply to join the team and accept the team invitation with freedom.</li>
        </ul>

        <h3>Bin</h3>
        <ul class="help">
        <li>Delete and restore your files as you do in your locally operation. All necessary settings are provided.</li>
        </ul>
  </div>
</template>
<script type="text/ecmascript-6">
export default {
    name: 'HelpPage',
    data(){
        return {}
    }
}
</script>

<style>
.row h1{
    font-size: 32px;
    margin-top: 25px;
    margin-bottom: 12.5px;
    margin-left: 50px;
    color: #505050;
    font-weight: 500;
    line-height: 1.35;
    box-sizing: border-box;
}

.help li{
    margin-left: 50px;
    box-sizing: border-box;
    color: #5d6879;
    font-size: 16px;
    line-height: 1.5625;
    text-align: left; 
}
</style>