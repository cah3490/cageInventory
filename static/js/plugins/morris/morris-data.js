// Morris.js Charts sample data for SB Admin_inv template

$(function() {

    // Area Chart
    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2014-08-18 11:00',
            out: 0,
            missing: 0
        }, {
            period: '2014-08-18 12:00',
            out: 9,
            missing: 1
        }, {
            period: '2014-08-18 13:00',
            out: 18,
            missing: 2
        }, {
            period: '2014-08-18 14:00',
            out: 24,
            missing: 6
        }, {
            period: '2014-08-18 15:00',
            out: 38,
            missing: 2
        }, {
            period: '2014-08-18 16:00',
            out: 49,
            missing: 1
        }, {
            period: '2014-08-18 17:00',
            out: 45,
            missing: 0
        }, {
            period: '2014-08-18 18:00',
            out: 38,
            missing: 2
        }, {
            period: '2014-08-18 19:00',
            out: 19,
            missing: 1
        }, {
            period: '2014-08-18 20:00',
            out: 0,
            missing: 0
        }],
        xkey: 'period',
        ykeys: [ 'out', 'missing'],
        labels: ['Out', 'Missing'],
        lineColors: ['orange','red'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });
});
