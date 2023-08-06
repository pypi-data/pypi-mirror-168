const m=function(){var a=[{defaultValue:null,kind:"LocalArgument",name:"name"},{defaultValue:null,kind:"LocalArgument",name:"view"}],l={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},n={alias:null,args:null,kind:"ScalarField",name:"mediaType",storageKey:null},i=[{alias:null,args:null,kind:"ScalarField",name:"ftype",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"subfield",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"embeddedDocType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"path",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dbField",storageKey:null}],s=[{alias:null,args:null,kind:"ScalarField",name:"target",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"value",storageKey:null}],r={alias:null,args:null,kind:"ScalarField",name:"key",storageKey:null},e={alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"timestamp",storageKey:null},d={alias:null,args:null,kind:"ScalarField",name:"viewStages",storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"cls",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"labels",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"edges",storageKey:null},c=[{alias:null,args:[{kind:"Variable",name:"name",variableName:"name"},{kind:"Variable",name:"view",variableName:"view"}],concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},l,n,{alias:null,args:null,kind:"ScalarField",name:"defaultGroupSlice",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"groupField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"groupSlice",storageKey:null},{alias:null,args:null,concreteType:"Group",kind:"LinkedField",name:"groupMediaTypes",plural:!0,selections:[l,n],storageKey:null},{alias:null,args:null,concreteType:"DatasetAppConfig",kind:"LinkedField",name:"appConfig",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"gridMediaField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"mediaFields",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"plugins",storageKey:null},{alias:null,args:null,concreteType:"SidebarGroup",kind:"LinkedField",name:"sidebarGroups",plural:!0,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"paths",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"sampleFields",plural:!0,selections:i,storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"frameFields",plural:!0,selections:i,storageKey:null},{alias:null,args:null,concreteType:"NamedTargets",kind:"LinkedField",name:"maskTargets",plural:!0,selections:[l,{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"targets",plural:!0,selections:s,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"defaultMaskTargets",plural:!0,selections:s,storageKey:null},{alias:null,args:null,concreteType:"EvaluationRun",kind:"LinkedField",name:"evaluations",plural:!0,selections:[r,e,u,d,{alias:null,args:null,concreteType:"EvaluationRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[t,{alias:null,args:null,kind:"ScalarField",name:"predField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"gtField",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"BrainRun",kind:"LinkedField",name:"brainMethods",plural:!0,selections:[r,e,u,d,{alias:null,args:null,concreteType:"BrainRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[t,{alias:null,args:null,kind:"ScalarField",name:"embeddingsField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"method",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"patchesField",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"lastLoadedAt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},{alias:null,args:null,concreteType:"NamedKeypointSkeleton",kind:"LinkedField",name:"skeletons",plural:!0,selections:[l,g,o],storageKey:null},{alias:null,args:null,concreteType:"KeypointSkeleton",kind:"LinkedField",name:"defaultSkeleton",plural:!1,selections:[g,o],storageKey:null},e,{alias:null,args:null,kind:"ScalarField",name:"viewCls",storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:a,kind:"Fragment",metadata:null,name:"DatasetQuery",selections:c,type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:a,kind:"Operation",name:"DatasetQuery",selections:c},params:{cacheID:"5ba0dc4897f8e5b5025ab9a233490365",id:null,metadata:{},name:"DatasetQuery",operationKind:"query",text:`query DatasetQuery(
  $name: String!
  $view: BSONArray = null
) {
  dataset(name: $name, view: $view) {
    id
    name
    mediaType
    defaultGroupSlice
    groupField
    groupSlice
    groupMediaTypes {
      name
      mediaType
    }
    appConfig {
      gridMediaField
      mediaFields
      plugins
      sidebarGroups {
        name
        paths
      }
    }
    sampleFields {
      ftype
      subfield
      embeddedDocType
      path
      dbField
    }
    frameFields {
      ftype
      subfield
      embeddedDocType
      path
      dbField
    }
    maskTargets {
      name
      targets {
        target
        value
      }
    }
    defaultMaskTargets {
      target
      value
    }
    evaluations {
      key
      version
      timestamp
      viewStages
      config {
        cls
        predField
        gtField
      }
    }
    brainMethods {
      key
      version
      timestamp
      viewStages
      config {
        cls
        embeddingsField
        method
        patchesField
      }
    }
    lastLoadedAt
    createdAt
    skeletons {
      name
      labels
      edges
    }
    defaultSkeleton {
      labels
      edges
    }
    version
    viewCls
  }
}
`}}}();m.hash="447724e7d4d6ce2853d339b3bd3ae577";export{m as default};
