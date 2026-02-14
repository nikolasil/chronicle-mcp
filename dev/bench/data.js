window.BENCHMARK_DATA = {
  "lastUpdate": 1771109402015,
  "repoUrl": "https://github.com/nikolasil/chronicle-mcp",
  "entries": {
    "Python Benchmark": [
      {
        "commit": {
          "author": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "id": "89344ee2dc736c40cce36a49be24274bc9122b6d",
          "message": "Refactor/service layer",
          "timestamp": "2026-02-12T22:16:20Z",
          "url": "https://github.com/nikolasil/chronicle-mcp/pull/7/commits/89344ee2dc736c40cce36a49be24274bc9122b6d"
        },
        "date": 1771007450064,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 202997.33120407932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017560946983814427",
            "extra": "mean: 4.926173137688544 usec\nrounds: 16149"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206040.18947180183,
            "unit": "iter/sec",
            "range": "stddev: 7.525074787073789e-7",
            "extra": "mean: 4.853422055976403 usec\nrounds: 35827"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202891.97657641274,
            "unit": "iter/sec",
            "range": "stddev: 7.617671230165135e-7",
            "extra": "mean: 4.92873112517282 usec\nrounds: 36954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 298405.47058101237,
            "unit": "iter/sec",
            "range": "stddev: 7.246965013582401e-7",
            "extra": "mean: 3.3511449976199943 usec\nrounds: 41780"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 435752.2957642214,
            "unit": "iter/sec",
            "range": "stddev: 5.757586083173463e-7",
            "extra": "mean: 2.2948817704934914 usec\nrounds: 97666"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449418.9154257366,
            "unit": "iter/sec",
            "range": "stddev: 5.482903688907929e-7",
            "extra": "mean: 2.225095485918067 usec\nrounds: 92422"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5819617.026295126,
            "unit": "iter/sec",
            "range": "stddev: 2.2007055255821924e-8",
            "extra": "mean: 171.83261295065682 nsec\nrounds: 193462"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52629.937139457485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020232195644447022",
            "extra": "mean: 19.00059271114509 usec\nrounds: 13747"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88742.52386070734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013202850647986294",
            "extra": "mean: 11.268554876460657 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20702.7881894456,
            "unit": "iter/sec",
            "range": "stddev: 0.000005408257895010322",
            "extra": "mean: 48.302672608600886 usec\nrounds: 7349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43765.25823914715,
            "unit": "iter/sec",
            "range": "stddev: 0.000002736394966006844",
            "extra": "mean: 22.84917398489197 usec\nrounds: 16944"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9182.772533066312,
            "unit": "iter/sec",
            "range": "stddev: 0.000004945935025387477",
            "extra": "mean: 108.89957214981561 usec\nrounds: 4754"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4466.392076703203,
            "unit": "iter/sec",
            "range": "stddev: 0.00006599150311584468",
            "extra": "mean: 223.89436100247926 usec\nrounds: 1795"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19525.21652020451,
            "unit": "iter/sec",
            "range": "stddev: 0.000005236560496958765",
            "extra": "mean: 51.21582129269651 usec\nrounds: 9731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1894258.5681440348,
            "unit": "iter/sec",
            "range": "stddev: 8.193633336638417e-8",
            "extra": "mean: 527.9110343313853 nsec\nrounds: 183790"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244322.00202718773,
            "unit": "iter/sec",
            "range": "stddev: 7.919792571198925e-7",
            "extra": "mean: 4.0929592574667994 usec\nrounds: 30165"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1752441.5922098642,
            "unit": "iter/sec",
            "range": "stddev: 5.640844953347712e-8",
            "extra": "mean: 570.6324276059266 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1280927.4725196338,
            "unit": "iter/sec",
            "range": "stddev: 1.1642029932570624e-7",
            "extra": "mean: 780.6843255792944 nsec\nrounds: 156446"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285534.43603118,
            "unit": "iter/sec",
            "range": "stddev: 6.425512446051044e-7",
            "extra": "mean: 3.5022045463223956 usec\nrounds: 53494"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148176.23770617234,
            "unit": "iter/sec",
            "range": "stddev: 9.809295161225622e-7",
            "extra": "mean: 6.748720412128163 usec\nrounds: 23971"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64302.6170520847,
            "unit": "iter/sec",
            "range": "stddev: 0.00040582778902836287",
            "extra": "mean: 15.551466578568746 usec\nrounds: 23458"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7970209.8373584775,
            "unit": "iter/sec",
            "range": "stddev: 1.0913893488205951e-8",
            "extra": "mean: 125.46721107805598 nsec\nrounds: 77919"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4cbb0b8538ecab84619aa23bdb3c8494121c84e4",
          "message": "Merge pull request #7 from nikolasil/refactor/service-layer\n\nRefactor/service layer",
          "timestamp": "2026-02-13T13:33:08-05:00",
          "tree_id": "2a3e9dbd387d8c855be01f4b1ac87a35836b4fc0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/4cbb0b8538ecab84619aa23bdb3c8494121c84e4"
        },
        "date": 1771007679329,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 200808.2875622288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019048679059906653",
            "extra": "mean: 4.979874148322232 usec\nrounds: 13063"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207330.1396613699,
            "unit": "iter/sec",
            "range": "stddev: 7.505177733293075e-7",
            "extra": "mean: 4.823225420256261 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 200241.04425699532,
            "unit": "iter/sec",
            "range": "stddev: 8.12884800413658e-7",
            "extra": "mean: 4.993981147624112 usec\nrounds: 36388"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 310389.9271689967,
            "unit": "iter/sec",
            "range": "stddev: 7.405135768448365e-7",
            "extra": "mean: 3.221754034097679 usec\nrounds: 43876"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440011.87176501437,
            "unit": "iter/sec",
            "range": "stddev: 5.640474272792331e-7",
            "extra": "mean: 2.2726659532814693 usec\nrounds: 100929"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446610.9077901452,
            "unit": "iter/sec",
            "range": "stddev: 5.281128473963275e-7",
            "extra": "mean: 2.2390854825916677 usec\nrounds: 101740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5631880.271195269,
            "unit": "iter/sec",
            "range": "stddev: 2.3056617217610387e-8",
            "extra": "mean: 177.5605928830627 nsec\nrounds: 199204"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52373.75076291122,
            "unit": "iter/sec",
            "range": "stddev: 0.000002008855059472649",
            "extra": "mean: 19.093534173766987 usec\nrounds: 13168"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 90209.09779784486,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013583795135008357",
            "extra": "mean: 11.085356404305935 usec\nrounds: 37623"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20585.567556744838,
            "unit": "iter/sec",
            "range": "stddev: 0.000004875017544676315",
            "extra": "mean: 48.577723069498326 usec\nrounds: 6164"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43493.46189266131,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027291263616138",
            "extra": "mean: 22.991961469241673 usec\nrounds: 17233"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9178.825476446713,
            "unit": "iter/sec",
            "range": "stddev: 0.000005434594459993481",
            "extra": "mean: 108.94640088386535 usec\nrounds: 4752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4508.173256441382,
            "unit": "iter/sec",
            "range": "stddev: 0.00006537266338557622",
            "extra": "mean: 221.81933637336962 usec\nrounds: 1864"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19672.74710999772,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052376695319537485",
            "extra": "mean: 50.83174171907078 usec\nrounds: 9540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1944753.7912538168,
            "unit": "iter/sec",
            "range": "stddev: 8.032113317932895e-8",
            "extra": "mean: 514.2039082259778 nsec\nrounds: 169751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244731.40820410478,
            "unit": "iter/sec",
            "range": "stddev: 8.287741823724674e-7",
            "extra": "mean: 4.086112229477325 usec\nrounds: 33182"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1762648.7385354755,
            "unit": "iter/sec",
            "range": "stddev: 5.44141491824896e-8",
            "extra": "mean: 567.3280093405649 nsec\nrounds: 67440"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292812.3294619953,
            "unit": "iter/sec",
            "range": "stddev: 1.3232814608585377e-7",
            "extra": "mean: 773.5074745273631 nsec\nrounds: 151470"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284487.41700296977,
            "unit": "iter/sec",
            "range": "stddev: 6.924620226701099e-7",
            "extra": "mean: 3.5150939557708485 usec\nrounds: 45266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146310.65029709705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010286082094838608",
            "extra": "mean: 6.834772437750836 usec\nrounds: 24345"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 63452.155448542115,
            "unit": "iter/sec",
            "range": "stddev: 0.00043934527866291685",
            "extra": "mean: 15.75990591542586 usec\nrounds: 22044"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8234385.5723038735,
            "unit": "iter/sec",
            "range": "stddev: 1.0580355279622409e-8",
            "extra": "mean: 121.44196931510291 nsec\nrounds: 80561"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "409a6768cf8c4075c25d0c008a5c21783fb8c314",
          "message": "Merge pull request #13 from nikolasil/add-create-release-workflow\n\nfix: resolve benchmark CI issues - permissions and summary size",
          "timestamp": "2026-02-14T17:41:19-05:00",
          "tree_id": "ba50a905654fc7f1ac847d3328722d06ef34b04c",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/409a6768cf8c4075c25d0c008a5c21783fb8c314"
        },
        "date": 1771109020499,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205362.0845073412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019433236856921686",
            "extra": "mean: 4.869448040513303 usec\nrounds: 15387"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 199792.90036397145,
            "unit": "iter/sec",
            "range": "stddev: 8.628921893569579e-7",
            "extra": "mean: 5.005182857740472 usec\nrounds: 37953"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 199457.81935250942,
            "unit": "iter/sec",
            "range": "stddev: 7.588183880757218e-7",
            "extra": "mean: 5.013591361051942 usec\nrounds: 22225"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307808.08899384993,
            "unit": "iter/sec",
            "range": "stddev: 7.092553869127156e-7",
            "extra": "mean: 3.248777520008515 usec\nrounds: 46993"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 429351.3573702524,
            "unit": "iter/sec",
            "range": "stddev: 7.206584354511035e-7",
            "extra": "mean: 2.3290947678026024 usec\nrounds: 95887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 444335.31979406724,
            "unit": "iter/sec",
            "range": "stddev: 5.919508959134003e-7",
            "extra": "mean: 2.2505525792175662 usec\nrounds: 88961"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5896288.28967601,
            "unit": "iter/sec",
            "range": "stddev: 2.480576914085623e-8",
            "extra": "mean: 169.59822024828694 nsec\nrounds: 197668"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51290.07430920149,
            "unit": "iter/sec",
            "range": "stddev: 0.000002427245356390301",
            "extra": "mean: 19.496949721139302 usec\nrounds: 12192"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89801.00653812608,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014137028914283343",
            "extra": "mean: 11.135732644326634 usec\nrounds: 34254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21161.830840551873,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053282094341712965",
            "extra": "mean: 47.25489054017603 usec\nrounds: 6998"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42486.351355288556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027316670619846786",
            "extra": "mean: 23.536970535256927 usec\nrounds: 16664"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8939.083080321707,
            "unit": "iter/sec",
            "range": "stddev: 0.000006221859231776179",
            "extra": "mean: 111.86829689516783 usec\nrounds: 4638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4523.903568452108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000633630977612194",
            "extra": "mean: 221.04803625205446 usec\nrounds: 1793"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20062.91229435159,
            "unit": "iter/sec",
            "range": "stddev: 0.00000547371818698063",
            "extra": "mean: 49.8432124573228 usec\nrounds: 9376"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1911245.1254295434,
            "unit": "iter/sec",
            "range": "stddev: 9.774422904748071e-8",
            "extra": "mean: 523.219123855319 nsec\nrounds: 178891"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242871.69515740924,
            "unit": "iter/sec",
            "range": "stddev: 8.708289845958605e-7",
            "extra": "mean: 4.117400339104494 usec\nrounds: 27719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1780456.6514909521,
            "unit": "iter/sec",
            "range": "stddev: 5.986226651134169e-8",
            "extra": "mean: 561.6536629310203 nsec\nrounds: 67719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296348.9989585334,
            "unit": "iter/sec",
            "range": "stddev: 1.2804161625415156e-7",
            "extra": "mean: 771.3972092416909 nsec\nrounds: 158153"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285653.4244624677,
            "unit": "iter/sec",
            "range": "stddev: 7.415584772994445e-7",
            "extra": "mean: 3.5007457091815506 usec\nrounds: 39561"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148316.0368968774,
            "unit": "iter/sec",
            "range": "stddev: 9.76533882593632e-7",
            "extra": "mean: 6.7423592277839095 usec\nrounds: 23879"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64619.09341346847,
            "unit": "iter/sec",
            "range": "stddev: 0.0004206903400349637",
            "extra": "mean: 15.475302223778511 usec\nrounds: 23294"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8033020.602997869,
            "unit": "iter/sec",
            "range": "stddev: 1.1179051547207441e-8",
            "extra": "mean: 124.48617393404739 nsec\nrounds: 78846"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3baac68beccd66a7867ba0300e88961d2188cbca",
          "message": "Merge pull request #14 from nikolasil/add-create-release-workflow\n\nfix: add -u flag to git-cliff for unreleased changelog",
          "timestamp": "2026-02-14T17:47:31-05:00",
          "tree_id": "e415ca443adcd028720ece55d6a3d6b541a8a52d",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/3baac68beccd66a7867ba0300e88961d2188cbca"
        },
        "date": 1771109401715,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 203408.0796334615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017262201901549167",
            "extra": "mean: 4.916225558994442 usec\nrounds: 16683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 203542.28943985893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017462260552939167",
            "extra": "mean: 4.912983944279905 usec\nrounds: 37370"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 201149.4249694333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018760302717217328",
            "extra": "mean: 4.971428579286071 usec\nrounds: 36348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 305879.75728789216,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010352629246409738",
            "extra": "mean: 3.269258511470591 usec\nrounds: 44323"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440804.68253454496,
            "unit": "iter/sec",
            "range": "stddev: 5.620824523797461e-7",
            "extra": "mean: 2.2685784421576147 usec\nrounds: 97097"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 445139.495621558,
            "unit": "iter/sec",
            "range": "stddev: 5.207945019973799e-7",
            "extra": "mean: 2.2464867975906704 usec\nrounds: 93809"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5803608.470246814,
            "unit": "iter/sec",
            "range": "stddev: 2.32248312092322e-8",
            "extra": "mean: 172.306592549558 nsec\nrounds: 191571"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50828.44191859647,
            "unit": "iter/sec",
            "range": "stddev: 0.000002121789362182132",
            "extra": "mean: 19.67402427171651 usec\nrounds: 13184"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88676.84207460815,
            "unit": "iter/sec",
            "range": "stddev: 0.000001340983925426292",
            "extra": "mean: 11.276901348817216 usec\nrounds: 38702"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20041.09799400459,
            "unit": "iter/sec",
            "range": "stddev: 0.00000863691854116887",
            "extra": "mean: 49.89746571266483 usec\nrounds: 7408"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42475.491600550384,
            "unit": "iter/sec",
            "range": "stddev: 0.000002837277146623971",
            "extra": "mean: 23.542988257893228 usec\nrounds: 16692"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9117.118451045286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000073758847843022474",
            "extra": "mean: 109.68377841853629 usec\nrounds: 4161"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4429.050977097437,
            "unit": "iter/sec",
            "range": "stddev: 0.00006438162632966876",
            "extra": "mean: 225.782002774632 usec\nrounds: 1802"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19665.483551043108,
            "unit": "iter/sec",
            "range": "stddev: 0.000006440033227545329",
            "extra": "mean: 50.85051671393849 usec\nrounds: 9483"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1937023.6136432996,
            "unit": "iter/sec",
            "range": "stddev: 1.0446883217138329e-7",
            "extra": "mean: 516.2559676384736 nsec\nrounds: 177936"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243321.59898731302,
            "unit": "iter/sec",
            "range": "stddev: 8.314165081215542e-7",
            "extra": "mean: 4.1097872287619674 usec\nrounds: 36034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1782407.7208255033,
            "unit": "iter/sec",
            "range": "stddev: 6.209885917642776e-8",
            "extra": "mean: 561.0388623860118 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296322.4115729423,
            "unit": "iter/sec",
            "range": "stddev: 1.2313956087473613e-7",
            "extra": "mean: 771.4130304872278 nsec\nrounds: 159439"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285465.9012368432,
            "unit": "iter/sec",
            "range": "stddev: 6.878285241283235e-7",
            "extra": "mean: 3.503045357316871 usec\nrounds: 52340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146523.92159431972,
            "unit": "iter/sec",
            "range": "stddev: 9.444376244882574e-7",
            "extra": "mean: 6.824824159216108 usec\nrounds: 28486"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 61556.668938089104,
            "unit": "iter/sec",
            "range": "stddev: 0.0004274572460545556",
            "extra": "mean: 16.245193530627112 usec\nrounds: 18178"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8107964.77657223,
            "unit": "iter/sec",
            "range": "stddev: 1.0624365973211877e-8",
            "extra": "mean: 123.33551360389123 nsec\nrounds: 80490"
          }
        ]
      }
    ]
  }
}