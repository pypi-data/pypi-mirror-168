const s=function(){var a={defaultValue:null,kind:"LocalArgument",name:"count"},l={defaultValue:null,kind:"LocalArgument",name:"cursor"},n={defaultValue:"",kind:"LocalArgument",name:"search"},e={alias:null,args:null,kind:"ScalarField",name:"colorscale",storageKey:null},r=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:[a,l,n],kind:"Fragment",metadata:null,name:"RootQuery",selections:[{args:null,kind:"FragmentSpread",name:"RootConfig_query"},{args:null,kind:"FragmentSpread",name:"RootDatasets_query"},{args:null,kind:"FragmentSpread",name:"RootGA_query"},{args:null,kind:"FragmentSpread",name:"RootNav_query"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[n,a,l],kind:"Operation",name:"RootQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"colorBy",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"colorPool",storageKey:null},e,{alias:null,args:null,kind:"ScalarField",name:"gridZoom",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"loopVideos",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"notebookHeight",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"plugins",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showConfidence",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showIndex",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showSkeletons",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showTooltip",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"timezone",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"useFrameNumber",storageKey:null}],storageKey:null},e,{alias:null,args:r,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:r,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"},{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"teamsSubmission",storageKey:null}]},params:{cacheID:"42eabc83fdab1de44494830c776ea037",id:null,metadata:{},name:"RootQuery",operationKind:"query",text:`query RootQuery(
  $search: String = ""
  $count: Int
  $cursor: String
) {
  ...RootConfig_query
  ...RootDatasets_query
  ...RootGA_query
  ...RootNav_query
}

fragment RootConfig_query on Query {
  config {
    colorBy
    colorPool
    colorscale
    gridZoom
    loopVideos
    notebookHeight
    plugins
    showConfidence
    showIndex
    showLabel
    showSkeletons
    showTooltip
    timezone
    useFrameNumber
  }
  colorscale
}

fragment RootDatasets_query on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment RootGA_query on Query {
  context
  dev
  doNotTrack
  uid
  version
}

fragment RootNav_query on Query {
  teamsSubmission
}
`}}}();s.hash="ad38dfd0504d23894ee801a4ba0ba91e";export{s as default};
