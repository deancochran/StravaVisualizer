
const getTooltip = a => `
<div style="text-align: center">
    <div><b>${a.name}</b></div>
    <div><b>${a.type}</b></div>
    <div>distance: <em>${a.distance}</em></div>
    <div>elapsed_time: <em>${a.elapsed_time}</em></div>
</div>
`;


const myGlobe = Globe()
.globeImageUrl(globeimgurl)
.bumpImageUrl(bumpimgurl)
.pathsData(gData['pathsData'])
.pathPoints('paths')
.pathStroke(4)
.pathColor(() => ['rgba(255,69,0,.1)', 'rgba(255,69,0,.1)'])
.pathDashAnimateTime(0)
.pathLabel(getTooltip)
.backgroundColor('#FF4500')
(document.getElementById('globeViz'));
myGlobe.controls().autoRotate = false;
myGlobe.controls().enabled = true;