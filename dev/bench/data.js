window.BENCHMARK_DATA = {
  "lastUpdate": 1771203819818,
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
          "id": "e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e",
          "message": "Merge pull request #15 from nikolasil/add-create-release-workflow\n\nfix: remove conflicting OUTPUT env from git-cliff action",
          "timestamp": "2026-02-14T17:50:49-05:00",
          "tree_id": "ed0ac0ba34f6fca055316a5ffeec09f966f4c359",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e"
        },
        "date": 1771109598432,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 208528.27298638807,
            "unit": "iter/sec",
            "range": "stddev: 0.000001787346377211716",
            "extra": "mean: 4.79551278912321 usec\nrounds: 15521"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 209099.04187807778,
            "unit": "iter/sec",
            "range": "stddev: 7.706914089602418e-7",
            "extra": "mean: 4.782422678833141 usec\nrounds: 38450"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203450.45938345033,
            "unit": "iter/sec",
            "range": "stddev: 6.964351115507064e-7",
            "extra": "mean: 4.915201484579911 usec\nrounds: 36509"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 306044.0704860228,
            "unit": "iter/sec",
            "range": "stddev: 7.504951945598198e-7",
            "extra": "mean: 3.2675032664802783 usec\nrounds: 43778"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433952.18143407936,
            "unit": "iter/sec",
            "range": "stddev: 4.928693710856227e-7",
            "extra": "mean: 2.3044013667480723 usec\nrounds: 41852"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439237.20982783375,
            "unit": "iter/sec",
            "range": "stddev: 5.361086217413561e-7",
            "extra": "mean: 2.27667414696484 usec\nrounds: 97857"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5670318.081316582,
            "unit": "iter/sec",
            "range": "stddev: 2.1879280076523074e-8",
            "extra": "mean: 176.3569495853478 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51458.299214892904,
            "unit": "iter/sec",
            "range": "stddev: 0.000002169957554326658",
            "extra": "mean: 19.433211265377054 usec\nrounds: 12605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 86270.1158141504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013304208891563058",
            "extra": "mean: 11.591499449870632 usec\nrounds: 39081"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21042.054647012363,
            "unit": "iter/sec",
            "range": "stddev: 0.000005203421215640608",
            "extra": "mean: 47.52387619818221 usec\nrounds: 7407"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42990.3051653305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028930897849841025",
            "extra": "mean: 23.261058421293768 usec\nrounds: 16672"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9116.077588478012,
            "unit": "iter/sec",
            "range": "stddev: 0.000005553405707971126",
            "extra": "mean: 109.69630197793833 usec\nrounds: 4348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4476.774785869503,
            "unit": "iter/sec",
            "range": "stddev: 0.00005621957259855532",
            "extra": "mean: 223.3750965441463 usec\nrounds: 1823"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19879.507281720256,
            "unit": "iter/sec",
            "range": "stddev: 0.000005723391590114814",
            "extra": "mean: 50.303057607445176 usec\nrounds: 9287"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1872453.411784999,
            "unit": "iter/sec",
            "range": "stddev: 7.73961645457176e-8",
            "extra": "mean: 534.0586813568102 nsec\nrounds: 181160"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245964.92103837573,
            "unit": "iter/sec",
            "range": "stddev: 6.689949080360651e-7",
            "extra": "mean: 4.065620397324783 usec\nrounds: 33975"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1767339.755804413,
            "unit": "iter/sec",
            "range": "stddev: 5.344316866884398e-8",
            "extra": "mean: 565.8221610845975 nsec\nrounds: 69604"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1283862.8895685463,
            "unit": "iter/sec",
            "range": "stddev: 1.1480335842344425e-7",
            "extra": "mean: 778.8993732314013 nsec\nrounds: 157208"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287795.3654385482,
            "unit": "iter/sec",
            "range": "stddev: 6.554021373580427e-7",
            "extra": "mean: 3.4746911176841935 usec\nrounds: 53263"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146941.18472539005,
            "unit": "iter/sec",
            "range": "stddev: 9.430000792733426e-7",
            "extra": "mean: 6.805443973170916 usec\nrounds: 17447"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65021.19507943279,
            "unit": "iter/sec",
            "range": "stddev: 0.0003890968670892543",
            "extra": "mean: 15.379600433033497 usec\nrounds: 23553"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8060605.814442196,
            "unit": "iter/sec",
            "range": "stddev: 1.0656761987866767e-8",
            "extra": "mean: 124.06015416473339 nsec\nrounds: 80109"
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
          "id": "83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1",
          "message": "Merge pull request #16 from nikolasil/add-create-release-workflow\n\nAdd create release workflow",
          "timestamp": "2026-02-14T18:14:52-05:00",
          "tree_id": "26b68aec8c7051f7d86d83354ac33915bea68313",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1"
        },
        "date": 1771111057795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207330.571012988,
            "unit": "iter/sec",
            "range": "stddev: 0.000001629079327257537",
            "extra": "mean: 4.823215385527281 usec\nrounds: 16756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206169.5988738288,
            "unit": "iter/sec",
            "range": "stddev: 7.799387899403793e-7",
            "extra": "mean: 4.850375639581943 usec\nrounds: 37134"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 204037.61647688737,
            "unit": "iter/sec",
            "range": "stddev: 7.213987721334858e-7",
            "extra": "mean: 4.901057056375074 usec\nrounds: 36350"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307385.15280343307,
            "unit": "iter/sec",
            "range": "stddev: 6.477380283718603e-7",
            "extra": "mean: 3.253247565406911 usec\nrounds: 41383"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 436283.6942086843,
            "unit": "iter/sec",
            "range": "stddev: 5.778368017591622e-7",
            "extra": "mean: 2.2920865786968365 usec\nrounds: 99424"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449161.53889163287,
            "unit": "iter/sec",
            "range": "stddev: 5.039932745523242e-7",
            "extra": "mean: 2.2263705001715772 usec\nrounds: 100726"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5667810.905806347,
            "unit": "iter/sec",
            "range": "stddev: 2.1907228900039464e-8",
            "extra": "mean: 176.4349616842714 nsec\nrounds: 196503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51170.85378507489,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018188170889435011",
            "extra": "mean: 19.542374731524845 usec\nrounds: 13503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88430.11618104897,
            "unit": "iter/sec",
            "range": "stddev: 0.000001337682484796155",
            "extra": "mean: 11.30836465206754 usec\nrounds: 38039"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20650.95485971584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050018418530077734",
            "extra": "mean: 48.42391099070759 usec\nrounds: 6460"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43048.505882359364,
            "unit": "iter/sec",
            "range": "stddev: 0.000002681096449263409",
            "extra": "mean: 23.229609936585167 usec\nrounds: 17028"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9122.272062402493,
            "unit": "iter/sec",
            "range": "stddev: 0.000005119047160298192",
            "extra": "mean: 109.62181276323767 usec\nrounds: 4748"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4572.556431293821,
            "unit": "iter/sec",
            "range": "stddev: 0.00008171799478438444",
            "extra": "mean: 218.69604345529015 usec\nrounds: 1887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19925.129966645083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051418290933210255",
            "extra": "mean: 50.187878406515416 usec\nrounds: 9614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1902152.9854296376,
            "unit": "iter/sec",
            "range": "stddev: 7.128968434922987e-8",
            "extra": "mean: 525.7200696578728 nsec\nrounds: 165810"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244610.84693145027,
            "unit": "iter/sec",
            "range": "stddev: 6.83207942322872e-7",
            "extra": "mean: 4.088126150351132 usec\nrounds: 35751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1760525.3654830311,
            "unit": "iter/sec",
            "range": "stddev: 5.3048579697090125e-8",
            "extra": "mean: 568.012264751356 nsec\nrounds: 69076"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1288313.6030201537,
            "unit": "iter/sec",
            "range": "stddev: 1.2493132266147712e-7",
            "extra": "mean: 776.2085238063752 nsec\nrounds: 159694"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286803.9505669032,
            "unit": "iter/sec",
            "range": "stddev: 6.33232583939544e-7",
            "extra": "mean: 3.4867023206039427 usec\nrounds: 52701"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149609.11112705618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010638300486103408",
            "extra": "mean: 6.684084896077925 usec\nrounds: 30449"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65363.42438619958,
            "unit": "iter/sec",
            "range": "stddev: 0.0003867421875957556",
            "extra": "mean: 15.299076041235283 usec\nrounds: 24513"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8030671.844448482,
            "unit": "iter/sec",
            "range": "stddev: 1.011019453184154e-8",
            "extra": "mean: 124.52258283872972 nsec\nrounds: 79854"
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
          "id": "38adc60ecea124b4e316f406a480d4d613bae342",
          "message": "Merge pull request #17 from nikolasil/add-create-release-workflow\n\nfix: add checkout step to create-tag job",
          "timestamp": "2026-02-15T13:54:25-05:00",
          "tree_id": "c49e81c1ba4aaf5c32005362933f3fe8edf8548f",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/38adc60ecea124b4e316f406a480d4d613bae342"
        },
        "date": 1771181814390,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207550.8123383504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016944569063453106",
            "extra": "mean: 4.818097258852424 usec\nrounds: 16708"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 208481.01814945097,
            "unit": "iter/sec",
            "range": "stddev: 7.922537567217035e-7",
            "extra": "mean: 4.796599752228491 usec\nrounds: 37132"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 189240.04091698487,
            "unit": "iter/sec",
            "range": "stddev: 0.000001818293481739528",
            "extra": "mean: 5.284293932480581 usec\nrounds: 37808"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 304655.21434910235,
            "unit": "iter/sec",
            "range": "stddev: 6.588057581796682e-7",
            "extra": "mean: 3.28239909543812 usec\nrounds: 43115"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431859.3753406785,
            "unit": "iter/sec",
            "range": "stddev: 6.311959006354689e-7",
            "extra": "mean: 2.315568578802152 usec\nrounds: 96349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 451433.74252458813,
            "unit": "iter/sec",
            "range": "stddev: 5.353556046227369e-7",
            "extra": "mean: 2.215164498798034 usec\nrounds: 102481"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5788890.448376119,
            "unit": "iter/sec",
            "range": "stddev: 2.2740088609152064e-8",
            "extra": "mean: 172.74467515284806 nsec\nrounds: 195351"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51903.349411595045,
            "unit": "iter/sec",
            "range": "stddev: 0.000001992531865789146",
            "extra": "mean: 19.26657935059203 usec\nrounds: 13705"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89357.3911252374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014164800450852272",
            "extra": "mean: 11.191016069375463 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21003.790768331073,
            "unit": "iter/sec",
            "range": "stddev: 0.000005679622811415642",
            "extra": "mean: 47.610453323871994 usec\nrounds: 7145"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43818.756792065695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029186520156320155",
            "extra": "mean: 22.82127730700637 usec\nrounds: 17230"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9148.116009330863,
            "unit": "iter/sec",
            "range": "stddev: 0.00000580182830279908",
            "extra": "mean: 109.31212492058731 usec\nrounds: 4715"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4433.219568403475,
            "unit": "iter/sec",
            "range": "stddev: 0.00006931590206135371",
            "extra": "mean: 225.56969817764465 usec\nrounds: 1756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20048.625359670696,
            "unit": "iter/sec",
            "range": "stddev: 0.000005683894878544157",
            "extra": "mean: 49.87873143719741 usec\nrounds: 9212"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1882809.9104479977,
            "unit": "iter/sec",
            "range": "stddev: 1.1447893324697614e-7",
            "extra": "mean: 531.1210624348472 nsec\nrounds: 166918"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244400.78121876897,
            "unit": "iter/sec",
            "range": "stddev: 7.872024027006686e-7",
            "extra": "mean: 4.091639948993764 usec\nrounds: 35295"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1768772.5006509735,
            "unit": "iter/sec",
            "range": "stddev: 6.104739323809657e-8",
            "extra": "mean: 565.3638326194358 nsec\nrounds: 69459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292761.1140022224,
            "unit": "iter/sec",
            "range": "stddev: 1.3171876786816895e-7",
            "extra": "mean: 773.5381186580872 nsec\nrounds: 180148"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285524.5803025271,
            "unit": "iter/sec",
            "range": "stddev: 6.869904240198872e-7",
            "extra": "mean: 3.5023254353108637 usec\nrounds: 53009"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148945.4276508274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010422373239017266",
            "extra": "mean: 6.713868399802772 usec\nrounds: 28389"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64338.20865254859,
            "unit": "iter/sec",
            "range": "stddev: 0.0004295810759936361",
            "extra": "mean: 15.542863578940937 usec\nrounds: 24549"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8129997.939265755,
            "unit": "iter/sec",
            "range": "stddev: 1.1010987655358637e-8",
            "extra": "mean: 123.00126118989931 nsec\nrounds: 77078"
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
          "id": "bdec3542dc3be0eca7c96d1dd5382dedb09fd247",
          "message": "Merge pull request #18 from nikolasil/add-create-release-workflow\n\nfix: use release files from prepare for building, only commit if chan…",
          "timestamp": "2026-02-15T14:17:32-05:00",
          "tree_id": "02399e607158f4023c19b085447af1972409040a",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/bdec3542dc3be0eca7c96d1dd5382dedb09fd247"
        },
        "date": 1771183203230,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 206401.73961688284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016267513041212174",
            "extra": "mean: 4.844920405497416 usec\nrounds: 17363"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 201607.20949982488,
            "unit": "iter/sec",
            "range": "stddev: 0.000001193045416302562",
            "extra": "mean: 4.960140078725054 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203621.60832020146,
            "unit": "iter/sec",
            "range": "stddev: 7.28371838248255e-7",
            "extra": "mean: 4.9110701376421115 usec\nrounds: 38567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 309758.00159627583,
            "unit": "iter/sec",
            "range": "stddev: 6.241820088898427e-7",
            "extra": "mean: 3.2283266125384986 usec\nrounds: 44340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431875.5355149708,
            "unit": "iter/sec",
            "range": "stddev: 5.186976049082276e-7",
            "extra": "mean: 2.3154819334871437 usec\nrounds: 106191"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439940.853038138,
            "unit": "iter/sec",
            "range": "stddev: 6.479633376784003e-7",
            "extra": "mean: 2.273032824967749 usec\nrounds: 108850"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5733330.514900015,
            "unit": "iter/sec",
            "range": "stddev: 2.3880585873637866e-8",
            "extra": "mean: 174.41869039316308 nsec\nrounds: 198020"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52226.08826654825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017891907380350666",
            "extra": "mean: 19.14751866722743 usec\nrounds: 10955"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87522.65902649522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015283689100013874",
            "extra": "mean: 11.42561264846028 usec\nrounds: 40005"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20846.487555179134,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858849089287324",
            "extra": "mean: 47.96971179691893 usec\nrounds: 7519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42648.98918852831,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025977931811164353",
            "extra": "mean: 23.447214553656508 usec\nrounds: 17329"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9121.822466620875,
            "unit": "iter/sec",
            "range": "stddev: 0.000004705256969197409",
            "extra": "mean: 109.62721579588514 usec\nrounds: 4824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4071.555111793739,
            "unit": "iter/sec",
            "range": "stddev: 0.00007782811018664732",
            "extra": "mean: 245.6064016187285 usec\nrounds: 1977"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19999.965064861855,
            "unit": "iter/sec",
            "range": "stddev: 0.000005027187564400521",
            "extra": "mean: 50.000087337997925 usec\nrounds: 9572"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1892373.9262112686,
            "unit": "iter/sec",
            "range": "stddev: 7.730462074865371e-8",
            "extra": "mean: 528.4367883899746 nsec\nrounds: 181819"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243444.13531141434,
            "unit": "iter/sec",
            "range": "stddev: 7.346428596176294e-7",
            "extra": "mean: 4.107718588992902 usec\nrounds: 36683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1730322.6922954987,
            "unit": "iter/sec",
            "range": "stddev: 6.162606189783092e-8",
            "extra": "mean: 577.9268829176427 nsec\nrounds: 67714"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1277736.689925303,
            "unit": "iter/sec",
            "range": "stddev: 1.2551219529877484e-7",
            "extra": "mean: 782.6338618002045 nsec\nrounds: 181786"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286497.57940331835,
            "unit": "iter/sec",
            "range": "stddev: 6.364290758703275e-7",
            "extra": "mean: 3.4904308863016436 usec\nrounds: 53752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147141.7154140971,
            "unit": "iter/sec",
            "range": "stddev: 9.688014409511808e-7",
            "extra": "mean: 6.796169238517615 usec\nrounds: 29875"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65753.26865256767,
            "unit": "iter/sec",
            "range": "stddev: 0.00037186540835013634",
            "extra": "mean: 15.208369416338513 usec\nrounds: 23954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8141804.73269818,
            "unit": "iter/sec",
            "range": "stddev: 1.0212498718917436e-8",
            "extra": "mean: 122.82289158626159 nsec\nrounds: 80174"
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
          "id": "a10a2f8736862a1295c5e305c1715a075c480fc5",
          "message": "Merge pull request #19 from nikolasil/add-create-release-workflow\n\nfix: checkout main before downloading release files in all jobs",
          "timestamp": "2026-02-15T14:30:24-05:00",
          "tree_id": "a9bdf56b1fd3ffd4006b93adec7ad9750a8932b8",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/a10a2f8736862a1295c5e305c1715a075c480fc5"
        },
        "date": 1771183972751,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 203780.43992652558,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017358279523272213",
            "extra": "mean: 4.9072423259099685 usec\nrounds: 18178"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 201827.29741657324,
            "unit": "iter/sec",
            "range": "stddev: 8.708937219259588e-7",
            "extra": "mean: 4.954731162732618 usec\nrounds: 35382"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 195236.84705510116,
            "unit": "iter/sec",
            "range": "stddev: 0.000001212794638620848",
            "extra": "mean: 5.121983965033879 usec\nrounds: 37356"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303740.5023092354,
            "unit": "iter/sec",
            "range": "stddev: 6.535016530991878e-7",
            "extra": "mean: 3.2922840134830267 usec\nrounds: 44600"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 427304.2136162723,
            "unit": "iter/sec",
            "range": "stddev: 5.243900802742915e-7",
            "extra": "mean: 2.3402530752903363 usec\nrounds: 103649"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 433185.2808863331,
            "unit": "iter/sec",
            "range": "stddev: 5.896855783687055e-7",
            "extra": "mean: 2.308481022148114 usec\nrounds: 106519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5359232.095813978,
            "unit": "iter/sec",
            "range": "stddev: 2.496013972996636e-8",
            "extra": "mean: 186.59389668561292 nsec\nrounds: 194175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 48945.6148951344,
            "unit": "iter/sec",
            "range": "stddev: 0.000002053037004642423",
            "extra": "mean: 20.430839456047128 usec\nrounds: 13311"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 85289.6218982818,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017762812949418184",
            "extra": "mean: 11.724755928600798 usec\nrounds: 38837"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20621.7967908335,
            "unit": "iter/sec",
            "range": "stddev: 0.000004752868679102774",
            "extra": "mean: 48.49237969624962 usec\nrounds: 7506"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42536.68727867516,
            "unit": "iter/sec",
            "range": "stddev: 0.000002941988282972408",
            "extra": "mean: 23.50911798675324 usec\nrounds: 17663"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9131.893806557955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059852522886036734",
            "extra": "mean: 109.50631064958975 usec\nrounds: 4188"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4429.5987236859955,
            "unit": "iter/sec",
            "range": "stddev: 0.00008168020558173784",
            "extra": "mean: 225.7540834687327 usec\nrounds: 1845"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 18369.71663178949,
            "unit": "iter/sec",
            "range": "stddev: 0.000013223463517556772",
            "extra": "mean: 54.43742111239005 usec\nrounds: 9691"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1847302.6250796563,
            "unit": "iter/sec",
            "range": "stddev: 8.817999168389839e-8",
            "extra": "mean: 541.3298213425373 nsec\nrounds: 183453"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 235450.8279165147,
            "unit": "iter/sec",
            "range": "stddev: 7.298797808779869e-7",
            "extra": "mean: 4.24717130472175 usec\nrounds: 24903"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1625507.7899452369,
            "unit": "iter/sec",
            "range": "stddev: 1.1506391945854966e-7",
            "extra": "mean: 615.1923763057704 nsec\nrounds: 140588"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1250577.4149199084,
            "unit": "iter/sec",
            "range": "stddev: 1.4236808687577618e-7",
            "extra": "mean: 799.630625077324 nsec\nrounds: 172682"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 277484.95913138933,
            "unit": "iter/sec",
            "range": "stddev: 6.877852582007982e-7",
            "extra": "mean: 3.6037989342928647 usec\nrounds: 55176"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 144504.36245218178,
            "unit": "iter/sec",
            "range": "stddev: 0.000001485741469769767",
            "extra": "mean: 6.920206304020143 usec\nrounds: 30552"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65402.57541136568,
            "unit": "iter/sec",
            "range": "stddev: 0.00034271340206417435",
            "extra": "mean: 15.289917770213982 usec\nrounds: 27788"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7891687.447632906,
            "unit": "iter/sec",
            "range": "stddev: 1.0675551192901561e-8",
            "extra": "mean: 126.71561141204339 nsec\nrounds: 78654"
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
          "id": "0d0bd73155a265381c7a28e6ebf5a8f0cad30b2f",
          "message": "Merge pull request #20 from nikolasil/add-create-release-workflow\n\nfix: correct workflow version output ref and PyPI publishing",
          "timestamp": "2026-02-15T14:47:57-05:00",
          "tree_id": "1dbd56af0284898405fdaf90caec915ff3f67fa0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/0d0bd73155a265381c7a28e6ebf5a8f0cad30b2f"
        },
        "date": 1771185030958,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 206260.73528538374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015811798263638507",
            "extra": "mean: 4.848232498620706 usec\nrounds: 17570"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207919.97556165775,
            "unit": "iter/sec",
            "range": "stddev: 7.833298379397218e-7",
            "extra": "mean: 4.80954269688943 usec\nrounds: 36361"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 198846.19270206647,
            "unit": "iter/sec",
            "range": "stddev: 7.856591294580494e-7",
            "extra": "mean: 5.02901255694803 usec\nrounds: 36872"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307196.7716714977,
            "unit": "iter/sec",
            "range": "stddev: 7.922823849289778e-7",
            "extra": "mean: 3.255242542292582 usec\nrounds: 44920"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433314.99355698534,
            "unit": "iter/sec",
            "range": "stddev: 5.950331963851703e-7",
            "extra": "mean: 2.3077899792740264 usec\nrounds: 97857"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446054.7860347139,
            "unit": "iter/sec",
            "range": "stddev: 5.566908896834396e-7",
            "extra": "mean: 2.2418770772300953 usec\nrounds: 102902"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5812432.22142708,
            "unit": "iter/sec",
            "range": "stddev: 2.182986915273529e-8",
            "extra": "mean: 172.0450169403157 nsec\nrounds: 199243"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52164.13014446599,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018412868542073848",
            "extra": "mean: 19.1702611973122 usec\nrounds: 13664"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89863.60950167189,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013143615080239007",
            "extra": "mean: 11.127975000619081 usec\nrounds: 37201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20865.950499701074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051321629836145654",
            "extra": "mean: 47.924967521337024 usec\nrounds: 7605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43097.04416543069,
            "unit": "iter/sec",
            "range": "stddev: 0.000002782250946407515",
            "extra": "mean: 23.20344746060629 usec\nrounds: 17130"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9123.647130108597,
            "unit": "iter/sec",
            "range": "stddev: 0.000005243246302499666",
            "extra": "mean: 109.60529114502232 usec\nrounds: 4314"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4521.094501835999,
            "unit": "iter/sec",
            "range": "stddev: 0.0000637418435650803",
            "extra": "mean: 221.18537880460227 usec\nrounds: 1840"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19851.035099887107,
            "unit": "iter/sec",
            "range": "stddev: 0.000005473454251408595",
            "extra": "mean: 50.37520688307519 usec\nrounds: 7613"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1754594.2144974296,
            "unit": "iter/sec",
            "range": "stddev: 1.2932691676194586e-7",
            "extra": "mean: 569.9323477403079 nsec\nrounds: 178254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 251122.20874374558,
            "unit": "iter/sec",
            "range": "stddev: 7.453245022474034e-7",
            "extra": "mean: 3.982124898480951 usec\nrounds: 36942"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1759438.1922029923,
            "unit": "iter/sec",
            "range": "stddev: 5.420645779680404e-8",
            "extra": "mean: 568.3632448310866 nsec\nrounds: 67079"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1268838.890380498,
            "unit": "iter/sec",
            "range": "stddev: 1.3230646353017796e-7",
            "extra": "mean: 788.12212297511 nsec\nrounds: 160206"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287181.5858164115,
            "unit": "iter/sec",
            "range": "stddev: 6.624664425288772e-7",
            "extra": "mean: 3.4821174106868984 usec\nrounds: 52508"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147415.115899604,
            "unit": "iter/sec",
            "range": "stddev: 9.500602769064472e-7",
            "extra": "mean: 6.783564859665022 usec\nrounds: 25162"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 66537.226135424,
            "unit": "iter/sec",
            "range": "stddev: 0.00036248108821933304",
            "extra": "mean: 15.029180777159064 usec\nrounds: 26198"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7997870.596753158,
            "unit": "iter/sec",
            "range": "stddev: 1.0596014856958723e-8",
            "extra": "mean: 125.03328078423105 nsec\nrounds: 80496"
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
          "id": "16b62eadb571582d44d6c3cbfa28c56243b702cb",
          "message": "Merge pull request #21 from nikolasil/add-create-release-workflow\n\nfix: add back PyPI password as fallback",
          "timestamp": "2026-02-15T14:58:48-05:00",
          "tree_id": "5048988938f1e257341aa95263221483fa3fd5d6",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/16b62eadb571582d44d6c3cbfa28c56243b702cb"
        },
        "date": 1771185689558,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205592.00480394004,
            "unit": "iter/sec",
            "range": "stddev: 0.000001616824718698237",
            "extra": "mean: 4.864002376715165 usec\nrounds: 16830"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207195.67764253725,
            "unit": "iter/sec",
            "range": "stddev: 7.265498964893752e-7",
            "extra": "mean: 4.826355507884881 usec\nrounds: 38272"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202793.45477684384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011088581700671555",
            "extra": "mean: 4.931125617936787 usec\nrounds: 36818"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 306510.29854331637,
            "unit": "iter/sec",
            "range": "stddev: 6.202239476253614e-7",
            "extra": "mean: 3.2625331179816097 usec\nrounds: 44266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433612.8996926275,
            "unit": "iter/sec",
            "range": "stddev: 5.534516205214282e-7",
            "extra": "mean: 2.3062044526555 usec\nrounds: 101647"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446696.82422980183,
            "unit": "iter/sec",
            "range": "stddev: 5.512275904089987e-7",
            "extra": "mean: 2.238654823042917 usec\nrounds: 102052"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5546297.652732137,
            "unit": "iter/sec",
            "range": "stddev: 3.3791232709504e-8",
            "extra": "mean: 180.30045673935868 nsec\nrounds: 195313"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51608.09168828878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018959222163913456",
            "extra": "mean: 19.37680637447259 usec\nrounds: 13397"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87747.8652645369,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013989286872383947",
            "extra": "mean: 11.396288638877552 usec\nrounds: 39468"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20666.604542333374,
            "unit": "iter/sec",
            "range": "stddev: 0.000005015261526541274",
            "extra": "mean: 48.38724222702403 usec\nrounds: 7526"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43216.0351313008,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025913986293668947",
            "extra": "mean: 23.13955912340772 usec\nrounds: 16973"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9201.722809338693,
            "unit": "iter/sec",
            "range": "stddev: 0.000005315209581735281",
            "extra": "mean: 108.67530143215298 usec\nrounds: 4817"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4519.6413973991885,
            "unit": "iter/sec",
            "range": "stddev: 0.0000622331401044548",
            "extra": "mean: 221.25649184810246 usec\nrounds: 1840"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19850.222828375034,
            "unit": "iter/sec",
            "range": "stddev: 0.000005334301673163735",
            "extra": "mean: 50.377268237540555 usec\nrounds: 9760"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1898041.4872157203,
            "unit": "iter/sec",
            "range": "stddev: 7.614379714860615e-8",
            "extra": "mean: 526.8588735997138 nsec\nrounds: 165536"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 248509.68816227582,
            "unit": "iter/sec",
            "range": "stddev: 7.182062140028615e-7",
            "extra": "mean: 4.023987987731907 usec\nrounds: 36629"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1769718.586421795,
            "unit": "iter/sec",
            "range": "stddev: 6.537387092907089e-8",
            "extra": "mean: 565.0615909628305 nsec\nrounds: 68933"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1269912.5271577218,
            "unit": "iter/sec",
            "range": "stddev: 1.3045889181927578e-7",
            "extra": "mean: 787.4558118094775 nsec\nrounds: 177905"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286430.15971891285,
            "unit": "iter/sec",
            "range": "stddev: 9.255477003874865e-7",
            "extra": "mean: 3.4912524609187323 usec\nrounds: 53434"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147229.30460444352,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010706286924308984",
            "extra": "mean: 6.792126083096497 usec\nrounds: 29084"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64938.78584869833,
            "unit": "iter/sec",
            "range": "stddev: 0.0003828367021969625",
            "extra": "mean: 15.399117598686125 usec\nrounds: 24286"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8075043.457752602,
            "unit": "iter/sec",
            "range": "stddev: 1.0809139278669759e-8",
            "extra": "mean: 123.83834281912411 nsec\nrounds: 78537"
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
          "id": "2f124043ea967ef582497af9e6a4c747fcbb7e2e",
          "message": "Merge pull request #22 from nikolasil/add-create-release-workflow\n\nfix: improve tag creation and explicitly set tag_name",
          "timestamp": "2026-02-15T15:16:52-05:00",
          "tree_id": "fa5e88fc922e40d2dc1931fb04daf156025f3ba4",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/2f124043ea967ef582497af9e6a4c747fcbb7e2e"
        },
        "date": 1771186762783,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205095.38528054924,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017310110075896936",
            "extra": "mean: 4.875780109006859 usec\nrounds: 13393"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 202730.09481515785,
            "unit": "iter/sec",
            "range": "stddev: 7.240631642524611e-7",
            "extra": "mean: 4.932666760264502 usec\nrounds: 39173"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 199601.7415541258,
            "unit": "iter/sec",
            "range": "stddev: 8.623412099843156e-7",
            "extra": "mean: 5.009976326929146 usec\nrounds: 38567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 305861.6358672312,
            "unit": "iter/sec",
            "range": "stddev: 6.65212979870765e-7",
            "extra": "mean: 3.2694522056178412 usec\nrounds: 43321"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 437243.4662764019,
            "unit": "iter/sec",
            "range": "stddev: 5.225280623570298e-7",
            "extra": "mean: 2.287055329873937 usec\nrounds: 98717"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 444649.17120522587,
            "unit": "iter/sec",
            "range": "stddev: 5.337258327554347e-7",
            "extra": "mean: 2.2489640479695265 usec\nrounds: 98242"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5800845.4149404755,
            "unit": "iter/sec",
            "range": "stddev: 2.1341202419895534e-8",
            "extra": "mean: 172.38866552537007 nsec\nrounds: 195695"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52616.88139067835,
            "unit": "iter/sec",
            "range": "stddev: 0.000002007640581366102",
            "extra": "mean: 19.00530730004764 usec\nrounds: 13726"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88432.91546051767,
            "unit": "iter/sec",
            "range": "stddev: 0.000001285274354500522",
            "extra": "mean: 11.30800669402861 usec\nrounds: 38243"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20406.02554338992,
            "unit": "iter/sec",
            "range": "stddev: 0.000005346833925990127",
            "extra": "mean: 49.005133208016 usec\nrounds: 7447"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42593.34590560187,
            "unit": "iter/sec",
            "range": "stddev: 0.000002661825132273206",
            "extra": "mean: 23.477845629133355 usec\nrounds: 17296"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9153.400585310492,
            "unit": "iter/sec",
            "range": "stddev: 0.000005205438642114593",
            "extra": "mean: 109.24901523536666 usec\nrounds: 4332"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4404.684982589624,
            "unit": "iter/sec",
            "range": "stddev: 0.00006239146291321517",
            "extra": "mean: 227.03099176279233 usec\nrounds: 1821"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19543.55751405885,
            "unit": "iter/sec",
            "range": "stddev: 0.000005273255290915882",
            "extra": "mean: 51.16775690815964 usec\nrounds: 8034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1891518.2816613368,
            "unit": "iter/sec",
            "range": "stddev: 8.227348022362892e-8",
            "extra": "mean: 528.6758313124509 nsec\nrounds: 184129"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242060.99338109206,
            "unit": "iter/sec",
            "range": "stddev: 7.424080073543875e-7",
            "extra": "mean: 4.131190184887147 usec\nrounds: 36454"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1764589.4672307058,
            "unit": "iter/sec",
            "range": "stddev: 5.347215044200841e-8",
            "extra": "mean: 566.7040513221937 nsec\nrounds: 68743"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1291876.9041598192,
            "unit": "iter/sec",
            "range": "stddev: 1.1938016249571582e-7",
            "extra": "mean: 774.067557659712 nsec\nrounds: 162814"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 279361.0524345405,
            "unit": "iter/sec",
            "range": "stddev: 6.317302170382283e-7",
            "extra": "mean: 3.5795970529367853 usec\nrounds: 54630"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147258.76770755125,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010109664519919922",
            "extra": "mean: 6.790767134395361 usec\nrounds: 30932"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64762.39854122342,
            "unit": "iter/sec",
            "range": "stddev: 0.00037695029421434963",
            "extra": "mean: 15.441058739717104 usec\nrounds: 23153"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8055374.4230166,
            "unit": "iter/sec",
            "range": "stddev: 1.066045956219878e-8",
            "extra": "mean: 124.1407223907214 nsec\nrounds: 80815"
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
          "id": "713f83daefb9d9288319b675cbff116e64705277",
          "message": "Merge pull request #24 from nikolasil/add-create-release-workflow\n\nAdd create release workflow",
          "timestamp": "2026-02-15T15:45:35-05:00",
          "tree_id": "fc40457edf775858e1c67d28a8275ed880abcfa5",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/713f83daefb9d9288319b675cbff116e64705277"
        },
        "date": 1771188488985,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 202347.42088548472,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016776568056232436",
            "extra": "mean: 4.941995285257102 usec\nrounds: 16756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 200263.79050199754,
            "unit": "iter/sec",
            "range": "stddev: 8.583137977381023e-7",
            "extra": "mean: 4.993413924171307 usec\nrounds: 34731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202303.86305678877,
            "unit": "iter/sec",
            "range": "stddev: 8.643980998416024e-7",
            "extra": "mean: 4.943059340983962 usec\nrounds: 37175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303063.7641635432,
            "unit": "iter/sec",
            "range": "stddev: 7.36273567220471e-7",
            "extra": "mean: 3.2996356484913423 usec\nrounds: 43856"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 419171.15932467877,
            "unit": "iter/sec",
            "range": "stddev: 5.821796314817649e-7",
            "extra": "mean: 2.3856603150156777 usec\nrounds: 91997"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 432166.7673014881,
            "unit": "iter/sec",
            "range": "stddev: 5.626665799781837e-7",
            "extra": "mean: 2.31392155913363 usec\nrounds: 94976"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5720440.948052431,
            "unit": "iter/sec",
            "range": "stddev: 4.0149766734826344e-8",
            "extra": "mean: 174.8116987975354 nsec\nrounds: 186220"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52526.849756910495,
            "unit": "iter/sec",
            "range": "stddev: 0.00000223969231359428",
            "extra": "mean: 19.037882618659022 usec\nrounds: 13503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 90479.17723802842,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014295247453135567",
            "extra": "mean: 11.052266726179953 usec\nrounds: 39205"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20155.231761576946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059362164051123396",
            "extra": "mean: 49.614909509815526 usec\nrounds: 5426"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 41536.17133959511,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031826131405538156",
            "extra": "mean: 24.07540145730119 usec\nrounds: 14410"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9031.21334754693,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054792117138173694",
            "extra": "mean: 110.72709297379419 usec\nrounds: 4711"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4476.522753760009,
            "unit": "iter/sec",
            "range": "stddev: 0.0000649408695436973",
            "extra": "mean: 223.38767275561378 usec\nrounds: 1916"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19055.865373476725,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059465787668571425",
            "extra": "mean: 52.477280900182535 usec\nrounds: 8398"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1904881.2176179425,
            "unit": "iter/sec",
            "range": "stddev: 8.484397024177078e-8",
            "extra": "mean: 524.9671164538851 nsec\nrounds: 178222"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 239558.61244391877,
            "unit": "iter/sec",
            "range": "stddev: 8.207240318041683e-7",
            "extra": "mean: 4.1743437641345595 usec\nrounds: 33171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1768358.0574691969,
            "unit": "iter/sec",
            "range": "stddev: 5.526048107601468e-8",
            "extra": "mean: 565.4963347361935 nsec\nrounds: 66721"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1102117.3800292776,
            "unit": "iter/sec",
            "range": "stddev: 3.8688040233420406e-7",
            "extra": "mean: 907.3443701372672 nsec\nrounds: 193051"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 279811.04101231194,
            "unit": "iter/sec",
            "range": "stddev: 7.397096831699454e-7",
            "extra": "mean: 3.573840390222483 usec\nrounds: 52785"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146423.48681112434,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010288502963401222",
            "extra": "mean: 6.829505441909926 usec\nrounds: 19203"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 59706.14858061177,
            "unit": "iter/sec",
            "range": "stddev: 0.0005062480702104644",
            "extra": "mean: 16.748693790721706 usec\nrounds: 20437"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8423919.76451283,
            "unit": "iter/sec",
            "range": "stddev: 1.1430978786194777e-8",
            "extra": "mean: 118.70958270672492 nsec\nrounds: 81813"
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
          "id": "b6c61f2a971bf77c97ba4cffb574930d0532f365",
          "message": "Merge pull request #25 from nikolasil/add-create-release-workflow\n\nfix: update homebrew formula URL version and fix summary step",
          "timestamp": "2026-02-15T17:55:49-05:00",
          "tree_id": "2957e0737af6a4bf673909ef625dea95c4da6102",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/b6c61f2a971bf77c97ba4cffb574930d0532f365"
        },
        "date": 1771196294713,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205697.74437193715,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015627737126931252",
            "extra": "mean: 4.861502021100566 usec\nrounds: 17812"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 209233.35248185848,
            "unit": "iter/sec",
            "range": "stddev: 8.66831997657079e-7",
            "extra": "mean: 4.779352756806326 usec\nrounds: 38287"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 205448.86263961522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010841879353950474",
            "extra": "mean: 4.86739126784135 usec\nrounds: 38112"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 312711.97616865975,
            "unit": "iter/sec",
            "range": "stddev: 6.483703346590189e-7",
            "extra": "mean: 3.197830835428748 usec\nrounds: 45104"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 439545.629514064,
            "unit": "iter/sec",
            "range": "stddev: 5.742838326371462e-7",
            "extra": "mean: 2.275076653828959 usec\nrounds: 95429"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446671.0047218826,
            "unit": "iter/sec",
            "range": "stddev: 5.551118806057648e-7",
            "extra": "mean: 2.2387842269337472 usec\nrounds: 100513"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5836094.994661243,
            "unit": "iter/sec",
            "range": "stddev: 2.3249818442948622e-8",
            "extra": "mean: 171.34745080654017 nsec\nrounds: 198808"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50719.22376131256,
            "unit": "iter/sec",
            "range": "stddev: 0.000002245954779224789",
            "extra": "mean: 19.71639007540917 usec\nrounds: 12595"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89260.07741063986,
            "unit": "iter/sec",
            "range": "stddev: 0.000001407539325575372",
            "extra": "mean: 11.20321681326258 usec\nrounds: 39112"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20621.316631040758,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057873968395247275",
            "extra": "mean: 48.493508823521225 usec\nrounds: 6120"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42930.04407986162,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026799621629224544",
            "extra": "mean: 23.29371006793579 usec\nrounds: 16935"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9135.920932906882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064045246778862555",
            "extra": "mean: 109.45804011920433 usec\nrounds: 4362"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4468.770436456921,
            "unit": "iter/sec",
            "range": "stddev: 0.00006014636537104721",
            "extra": "mean: 223.77520040900853 usec\nrounds: 1956"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19652.676366302552,
            "unit": "iter/sec",
            "range": "stddev: 0.000005714618174886038",
            "extra": "mean: 50.88365479394193 usec\nrounds: 9658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1560146.5769688396,
            "unit": "iter/sec",
            "range": "stddev: 2.5380093629716755e-7",
            "extra": "mean: 640.9654161744655 nsec\nrounds: 179824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 240546.94569555338,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010905736172858951",
            "extra": "mean: 4.157192672342817 usec\nrounds: 34172"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1779384.9744904952,
            "unit": "iter/sec",
            "range": "stddev: 5.3090399904641e-8",
            "extra": "mean: 561.9919322327924 nsec\nrounds: 69945"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1300895.393319403,
            "unit": "iter/sec",
            "range": "stddev: 1.3286475214905463e-7",
            "extra": "mean: 768.7013153672688 nsec\nrounds: 157928"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286673.6343714333,
            "unit": "iter/sec",
            "range": "stddev: 6.87419792914076e-7",
            "extra": "mean: 3.488287306897341 usec\nrounds: 53462"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 145748.97673224215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011058661030733599",
            "extra": "mean: 6.861111634678003 usec\nrounds: 26103"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64298.02330236112,
            "unit": "iter/sec",
            "range": "stddev: 0.0003950841639139377",
            "extra": "mean: 15.552577647644084 usec\nrounds: 22029"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8132354.289545932,
            "unit": "iter/sec",
            "range": "stddev: 1.0421853731636441e-8",
            "extra": "mean: 122.96562156499257 nsec\nrounds: 81150"
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
          "id": "19e5c93795896cdb71cf34ce25dbc5cfe62585db",
          "message": "Merge pull request #26 from nikolasil/add-create-release-workflow\n\nfix: combine version bump, Homebrew update, and tag into single atomi…",
          "timestamp": "2026-02-15T18:17:03-05:00",
          "tree_id": "fe89395b665a8e87938bbacf7e25796502819a99",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/19e5c93795896cdb71cf34ce25dbc5cfe62585db"
        },
        "date": 1771197593327,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 201948.58203883917,
            "unit": "iter/sec",
            "range": "stddev: 0.000001778806655363222",
            "extra": "mean: 4.951755490948077 usec\nrounds: 15480"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 205845.50839034485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011196031452645709",
            "extra": "mean: 4.858012243355342 usec\nrounds: 36428"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 204493.08701924814,
            "unit": "iter/sec",
            "range": "stddev: 7.351737256145682e-7",
            "extra": "mean: 4.890140857944376 usec\nrounds: 38301"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 304607.49057681405,
            "unit": "iter/sec",
            "range": "stddev: 6.49000321636615e-7",
            "extra": "mean: 3.282913358783034 usec\nrounds: 44540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 435887.75021543785,
            "unit": "iter/sec",
            "range": "stddev: 5.987350048477117e-7",
            "extra": "mean: 2.294168623701284 usec\nrounds: 105175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 450171.026528539,
            "unit": "iter/sec",
            "range": "stddev: 5.197420252246429e-7",
            "extra": "mean: 2.221377967639159 usec\nrounds: 106861"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5830072.358438981,
            "unit": "iter/sec",
            "range": "stddev: 3.244208722764683e-8",
            "extra": "mean: 171.52445776301852 nsec\nrounds: 179534"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51565.277941335444,
            "unit": "iter/sec",
            "range": "stddev: 0.000001930300110694295",
            "extra": "mean: 19.392894597362115 usec\nrounds: 13586"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 86518.01281555044,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012920015096022334",
            "extra": "mean: 11.558286736565725 usec\nrounds: 39688"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20734.598520812666,
            "unit": "iter/sec",
            "range": "stddev: 0.000005313920704787399",
            "extra": "mean: 48.22856825495005 usec\nrounds: 5897"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42709.74027862669,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026793439975231607",
            "extra": "mean: 23.413862820899237 usec\nrounds: 16832"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9099.39284007075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057374586978445275",
            "extra": "mean: 109.89744234322175 usec\nrounds: 4336"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4503.937318873005,
            "unit": "iter/sec",
            "range": "stddev: 0.00006248577102200713",
            "extra": "mean: 222.02795669683616 usec\nrounds: 1986"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19784.585604192675,
            "unit": "iter/sec",
            "range": "stddev: 0.00000563393536373264",
            "extra": "mean: 50.544399564683516 usec\nrounds: 9648"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1902143.174408349,
            "unit": "iter/sec",
            "range": "stddev: 7.896505971731583e-8",
            "extra": "mean: 525.7227812575546 nsec\nrounds: 186602"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243672.8181832476,
            "unit": "iter/sec",
            "range": "stddev: 8.422581469672511e-7",
            "extra": "mean: 4.103863563674044 usec\nrounds: 34419"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1751582.4003924285,
            "unit": "iter/sec",
            "range": "stddev: 6.56394129168901e-8",
            "extra": "mean: 570.9123360544901 nsec\nrounds: 69459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1258058.5246121273,
            "unit": "iter/sec",
            "range": "stddev: 1.2372614456177435e-7",
            "extra": "mean: 794.8755804571734 nsec\nrounds: 153328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 283637.7778775741,
            "unit": "iter/sec",
            "range": "stddev: 6.474878564462758e-7",
            "extra": "mean: 3.5256234465058736 usec\nrounds: 54072"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 145617.67936217465,
            "unit": "iter/sec",
            "range": "stddev: 8.960313437837509e-7",
            "extra": "mean: 6.86729801202805 usec\nrounds: 21932"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64986.90351466393,
            "unit": "iter/sec",
            "range": "stddev: 0.00039763323843017257",
            "extra": "mean: 15.387715769137326 usec\nrounds: 23305"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8128107.313337165,
            "unit": "iter/sec",
            "range": "stddev: 1.034870316960167e-8",
            "extra": "mean: 123.02987170948336 nsec\nrounds: 79663"
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
          "id": "4096cba46f9335921d287e572991a231f6d3044a",
          "message": "Merge pull request #27 from nikolasil/feature/docs-update-and-bookmarks\n\nFeature/docs update and bookmarks",
          "timestamp": "2026-02-15T20:01:06-05:00",
          "tree_id": "2ce7830072457d31dc30befc74c00c3b9d21fb23",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/4096cba46f9335921d287e572991a231f6d3044a"
        },
        "date": 1771203819359,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 199927.92324354197,
            "unit": "iter/sec",
            "range": "stddev: 0.000001168929942064372",
            "extra": "mean: 5.001802568527914 usec\nrounds: 24216"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 199057.77394550678,
            "unit": "iter/sec",
            "range": "stddev: 7.744760001144054e-7",
            "extra": "mean: 5.023667150391 usec\nrounds: 40658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 198714.0791278322,
            "unit": "iter/sec",
            "range": "stddev: 8.045048697576517e-7",
            "extra": "mean: 5.0323560584587606 usec\nrounds: 42420"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303090.67580515763,
            "unit": "iter/sec",
            "range": "stddev: 6.207621539179456e-7",
            "extra": "mean: 3.2993426714415057 usec\nrounds: 51081"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 427876.6523016834,
            "unit": "iter/sec",
            "range": "stddev: 5.492773558585955e-7",
            "extra": "mean: 2.337122146349152 usec\nrounds: 105742"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 432370.20652097336,
            "unit": "iter/sec",
            "range": "stddev: 5.195554605478354e-7",
            "extra": "mean: 2.312832810674924 usec\nrounds: 107782"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5796157.872651394,
            "unit": "iter/sec",
            "range": "stddev: 2.822721072733624e-8",
            "extra": "mean: 172.52808187271327 nsec\nrounds: 199641"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50002.98822575384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020986408035418415",
            "extra": "mean: 19.99880478113014 usec\nrounds: 13595"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87361.54176407636,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012619467960039055",
            "extra": "mean: 11.446684431240277 usec\nrounds: 38391"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20723.315946154984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052639202016583975",
            "extra": "mean: 48.25482575270685 usec\nrounds: 7805"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42956.923618117995,
            "unit": "iter/sec",
            "range": "stddev: 0.000002577364987518479",
            "extra": "mean: 23.279134439185697 usec\nrounds: 17242"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9179.942504710609,
            "unit": "iter/sec",
            "range": "stddev: 0.000004827786426267549",
            "extra": "mean: 108.93314413318586 usec\nrounds: 4926"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4497.660016741616,
            "unit": "iter/sec",
            "range": "stddev: 0.00006485641140359856",
            "extra": "mean: 222.33783707032217 usec\nrounds: 2007"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20001.473218181316,
            "unit": "iter/sec",
            "range": "stddev: 0.00000509232894730165",
            "extra": "mean: 49.996317225823205 usec\nrounds: 9747"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1880896.647974127,
            "unit": "iter/sec",
            "range": "stddev: 7.598075301341199e-8",
            "extra": "mean: 531.6613228467808 nsec\nrounds: 168606"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243356.13992714905,
            "unit": "iter/sec",
            "range": "stddev: 6.798843864873629e-7",
            "extra": "mean: 4.109203902968543 usec\nrounds: 37356"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1739883.5910409798,
            "unit": "iter/sec",
            "range": "stddev: 5.332562594639288e-8",
            "extra": "mean: 574.7510955039662 nsec\nrounds: 70196"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1257010.89306477,
            "unit": "iter/sec",
            "range": "stddev: 1.3021949558059392e-7",
            "extra": "mean: 795.5380542181045 nsec\nrounds: 178540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284360.26002885145,
            "unit": "iter/sec",
            "range": "stddev: 6.870699626087566e-7",
            "extra": "mean: 3.5166657953489673 usec\nrounds: 62740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148065.25826786627,
            "unit": "iter/sec",
            "range": "stddev: 9.482183638894585e-7",
            "extra": "mean: 6.753778784425517 usec\nrounds: 29912"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78759.48343908881,
            "unit": "iter/sec",
            "range": "stddev: 0.00005319494289056144",
            "extra": "mean: 12.696883680977699 usec\nrounds: 23874"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8016328.005925879,
            "unit": "iter/sec",
            "range": "stddev: 1.0538281295411063e-8",
            "extra": "mean: 124.74539455740172 nsec\nrounds: 79152"
          }
        ]
      }
    ]
  }
}