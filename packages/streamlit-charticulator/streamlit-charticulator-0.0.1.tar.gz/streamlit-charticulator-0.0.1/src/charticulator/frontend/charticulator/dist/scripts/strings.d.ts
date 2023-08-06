import { Region2DConfigurationTerminology } from "./core/prototypes/plot_segments/region_2d/base";
export declare const strings: {
    app: {
        loading: string;
        name: string;
        nestedChartTitle: string;
        working: string;
    };
    dialogs: {
        saveChanges: {
            saveChangesTitle: string;
            saveChanges: (chartName: string) => string;
        };
    };
    about: {
        version: (version: string, url: string) => string;
        license: string;
    };
    button: {
        cancel: string;
        no: string;
        yes: string;
    };
    canvas: {
        markContainer: string;
        newGlyph: string;
        zoomAuto: string;
        zoomIn: string;
        zoomOut: string;
        sublayoutType: string;
        elementOrders: string;
        gridDirection: string;
        alignItemsOnX: string;
        alignItemsOnY: string;
    };
    dataset: {
        dimensions: (rows: number, columns: number) => string;
        months: string[];
        replaceWithCSV: string;
        showDataValues: string;
        showDerivedFields: string;
        tableTitleColumns: string;
        tableTitleLinks: string;
        tableTitleImages: string;
        weekday: string[];
    };
    defaultDataset: {
        city: string;
        month: string;
        temperature: string;
        value: string;
    };
    dialog: {
        resetConfirm: string;
        deleteChart: string;
    };
    scaleEditor: {
        add: string;
        removeLast: string;
        addLegend: string;
        removeLegend: string;
        removeSelected: string;
        reverse: string;
    };
    legendCreator: {
        legendType: string;
        connectBy: string;
        createLegend: string;
    };
    mappingEditor: {
        bindData: string;
        keyColumnExpression: string;
        bindDataValue: string;
        remove: string;
        chooseColor: string;
    };
    error: {
        imageLoad: (url: string) => string;
        notImplemented: string;
        storeNotFound: (componentName: string) => string;
    };
    fileExport: {
        asHTML: string;
        asImage: string;
        inferAxisMin: (objectName: string, inferenceAxisProperty: string) => string;
        inferAxisMax: (objectName: string, inferenceAxisProperty: string) => string;
        inferScaleMin: (objectName: string) => string;
        inferScaleMax: (objectName: string) => string;
        imageDPI: string;
        labelAxesAndScales: string;
        labelExposedObjects: string;
        labelProperties: (exportKind: string) => string;
        labelSlots: string;
        slotColumnExample: (columnName: string) => string;
        slotColumnName: (columnName: string) => string;
        typeHTML: string;
        typeJPEG: string;
        typePNG: string;
        typeSVG: string;
    };
    fileImport: {
        doneButtonText: string;
        doneButtonTitle: string;
        fileUpload: string;
        loadSample: string;
        links: string;
        messageNoID: (keyColumn: string) => string;
        messageNoSourceOrTargetID: (linkSourceKeyColumn: string, linkTargetKeyColumn: string) => string;
        removeButtonText: string;
        removeButtonTitle: string;
    };
    fileOpen: {
        copy: string;
        deleteConfirmation: (chartName: string) => string;
        delete: string;
        download: string;
        open: string;
        noChart: string;
    };
    fileSave: {
        saveButton: string;
        chartName: string;
    };
    filter: {
        editFilter: string;
        filterBy: string;
        filterType: string;
        none: string;
        categories: string;
        expression: string;
        selectAll: string;
        clear: string;
        values: string;
        column: string;
    };
    handles: {
        drawSpiral: string;
        startAngle: string;
        windings: string;
    };
    help: {
        contact: string;
        gallery: string;
        gettingStarted: string;
        home: string;
        issues: string;
        version: (version: string) => string;
    };
    mainTabs: {
        about: string;
        export: string;
        new: string;
        open: string;
        options: string;
        save: string;
    };
    mainView: {
        attributesPaneltitle: string;
        datasetPanelTitle: string;
        errorsPanelTitle: string;
        glyphPaneltitle: string;
        layersPanelTitle: string;
        scalesPanelTitle: string;
    };
    menuBar: {
        defaultTemplateName: string;
        export: string;
        exportTemplate: string;
        copyTemplate: string;
        help: string;
        home: string;
        importTemplate: string;
        new: string;
        open: string;
        redo: string;
        reset: string;
        save: string;
        saveButton: string;
        dontSaveButton: string;
        cancel: string;
        savedButton: string;
        saveNested: string;
        editNestedChart: string;
        closeNested: string;
        undo: string;
    };
    options: {
        comma: string;
        delimiter: string;
        fileFormat: string;
        numberFormat: string;
        timeZone: string;
        currencyFormat: string;
        groups: string;
        numberFormatComma: string;
        numberFormatDot: string;
        semicolon: string;
        utc: string;
        local: string;
    };
    coordinateSystem: {
        x: string;
        y: string;
    };
    templateImport: {
        columnNameTemplate: string;
        columnNameChart: string;
        dataType: string;
        examples: string;
        mapped: string;
        save: string;
        tableName: string;
        title: string;
        usbtitleImportTemplate: string;
        usbtitleImportData: string;
        unmapped: string;
    };
    toolbar: {
        symbol: string;
        marks: string;
        curve: string;
        dataAxis: string;
        ellipse: string;
        icon: string;
        image: string;
        guides: string;
        guidePolar: string;
        guideX: string;
        guideY: string;
        legend: string;
        line: string;
        lineH: string;
        lineV: string;
        link: string;
        links: string;
        nestedChart: string;
        plot: string;
        plotSegments: string;
        polar: string;
        rectangle: string;
        region2D: string;
        scaffolds: string;
        text: string;
        textbox: string;
        triangle: string;
    };
    typeDisplayNames: {
        string: string;
        number: string;
        boolean: string;
        date: string;
        image: string;
    };
    attributesPanel: {
        conditionedBy: string;
    };
    core: {
        default: string;
        auto: string;
        none: string;
    };
    cartesianTerminology: Region2DConfigurationTerminology;
    curveTerminology: Region2DConfigurationTerminology;
    polarTerminology: Region2DConfigurationTerminology;
    alignment: {
        align: string;
        alignment: string;
        left: string;
        right: string;
        middle: string;
        center: string;
        top: string;
        bottom: string;
        padding: string;
    };
    margins: {
        margins: string;
        margin: string;
        left: string;
        right: string;
        top: string;
        bottom: string;
    };
    scale: {
        linear: string;
        logarithmic: string;
    };
    objects: {
        default: string;
        opposite: string;
        position: string;
        general: string;
        contextMenu: string;
        interactivity: string;
        colors: string;
        color: string;
        outline: string;
        dimensions: string;
        scale: string;
        width: string;
        height: string;
        background: string;
        opacity: string;
        font: string;
        fontSize: string;
        size: string;
        axis: string;
        style: string;
        rotation: string;
        anchorAndRotation: string;
        fill: string;
        strokeWidth: string;
        stroke: string;
        anchorX: string;
        anchorY: string;
        alignX: string;
        alignY: string;
        layout: string;
        appearance: string;
        visibilityAndPosition: string;
        onTop: string;
        invalidFormat: string;
        roundX: string;
        roundY: string;
        dropData: string;
        dropTickData: string;
        toolTips: string;
        selection: string;
        axes: {
            data: string;
            numericalSuffix: string;
            categoricalSuffix: string;
            stackingSuffix: string;
            tickFormat: string;
            tickData: string;
            ticksize: string;
            tickDataFormatType: string;
            tickDataFormatTypeNone: string;
            tickDataFormatTypeDate: string;
            tickDataFormatTypeNumber: string;
            from: string;
            to: string;
            gap: string;
            direction: string;
            count: string;
            dataExpressions: string;
            lineColor: string;
            tickColor: string;
            tickTextBackgroudColor: string;
            showTickLine: string;
            showBaseline: string;
            verticalText: string;
            offSet: string;
            orderBy: string;
            numberOfTicks: string;
            autoNumberOfTicks: string;
        };
        plotSegment: {
            subLayout: string;
            type: string;
            gridline: string;
            polarCoordinates: string;
            heightToArea: string;
            equalizeArea: string;
            autoAlignment: string;
            origin: string;
            inner: string;
            outer: string;
            radius: string;
            angle: string;
            curveCoordinates: string;
            normal: string;
            groupBy: string;
            groupByCategory: string;
            distribution: string;
            gravity: string;
            packingInContainer: string;
            packingX: string;
            packingY: string;
            order: string;
            reverseGlyphs: string;
            flipGrid: string;
            orientation: string;
            direction: string;
            directionDownRight: string;
            directionDownLeft: string;
            directionUpLeft: string;
            directionUpRight: string;
        };
        visibleOn: {
            visibility: string;
            label: string;
            all: string;
            first: string;
            last: string;
            visible: string;
        };
        guides: {
            guideCoordinator: string;
            count: string;
            guide: string;
            baseline: string;
            offset: string;
            angular: string;
            radial: string;
            angle: string;
        };
        legend: {
            orientation: string;
            vertical: string;
            horizontal: string;
            legend: string;
            editColors: string;
            markerShape: string;
            labels: string;
            layout: string;
            categoricalLegend: string;
            numericalColorLegend: string;
            ordering: string;
        };
        links: {
            lineType: string;
            type: string;
            line: string;
            bezier: string;
            arc: string;
            solid: string;
            dashed: string;
            dotted: string;
            linkMarkType: string;
            curveness: string;
            closeLink: string;
        };
        arrows: {
            beginArrowType: string;
            endArrowType: string;
            noArrow: string;
            arrow: string;
            diamondArrow: string;
            ovalArrow: string;
        };
        line: {
            lineStyle: string;
            xSpan: string;
            ySpan: string;
        };
        anchor: {
            label: string;
        };
        dataAxis: {
            dataExpression: string;
            autoUpdateValues: string;
            autoMin: string;
            autoMax: string;
            end: string;
            start: string;
            exportProperties: string;
            domain: string;
            range: string;
            gradient: string;
            scrolling: string;
            allowScrolling: string;
            windowSize: string;
            barOffset: string;
        };
        icon: {
            label: string;
            image: string;
            anchorAndRotation: string;
            anchorX: string;
            anchorY: string;
        };
        image: {
            imageMode: string;
            letterbox: string;
            stretch: string;
            dropImage: string;
            defaultPlaceholder: string;
        };
        scales: {
            mode: string;
            greater: string;
            less: string;
            interval: string;
            inclusive: string;
            imageMapping: string;
            stringMapping: string;
            colorMapping: string;
            numberMapping: string;
            booleanMapping: string;
            minimumValue: string;
            maximumValue: string;
            startDate: string;
            endDate: string;
            exportProperties: string;
            autoMin: string;
            autoMax: string;
            selectAll: string;
            clear: string;
            value: string;
            date: string;
        };
        text: {
            margin: string;
            wrapText: string;
            overflow: string;
            textDisplaying: string;
        };
        rect: {
            shape: string;
            flipping: string;
            shapes: {
                rectangle: string;
                triangle: string;
                ellipse: string;
                comet: string;
            };
        };
        derivedColumns: {
            year: string;
            month: string;
            monthNumber: string;
            day: string;
            weekOfYear: string;
            dayOfYear: string;
            weekday: string;
            hour: string;
            minute: string;
            second: string;
            menuSuffix: string;
        };
        nestedChart: {
            sizeAndShape: string;
        };
    };
    reOrder: {
        reverse: string;
        sort: string;
        reset: string;
    };
    panels: {
        collapseAllCategories: string;
        expandAllCategories: string;
    };
};
