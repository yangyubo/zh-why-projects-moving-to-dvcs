为什么软件项目从集中式迁移到分布式版本控制系统的热情持续不减?
===================================================================

译者 (yospaly) 前言:
  .. line-block::
    
    DVCS (分布式版本控制系统) 开始逐渐为开发者所接受, 很多开源项目对 DVCS 也是趋之若鹜. 相对于传统的 CVCS (集中式版本控制系统), DVCS 到底能够给软件开发带来哪些好处? 这么多大型开源项目迁移到 DVCS 到底是出于什么目的? 最重要的原因肯定不是赶时髦 :)
    
    两位来自加拿大萨省大学计算机科学院下属研究机构的研究员着手对这个现象进行一番深入探究, <<为什么迁移到 DVCS>> 是他们的初步研究成果, 主要研究对象是 4 个大型开源项目. 尽管是初步报告, <<为什么迁移到 DVCS>> 仍然有利于认识和理解 DVCS 流行现象.
    
    十分期待他们的后续研究成果, 尤其是商业公司切换到 DVCS 的部分, 对该系列后续论文的翻译我将尽力跟进.
    
    译文由强大的 reStructuredText_ 文本标记语法驱动.


英文版原作者:
  .. line-block::
    
    Brian de Alwis
    Dept of Computer Science
    University of Saskatchewan
    Saskatoon, SK, Canada
    brian.de.alwis@usask.ca
    
    Jonathan Sillito
    Dept of Computer Science
    University of Calgary
    Calgary, AB, Canada
    sillito@ucalgary.ca


.. _abstract:


摘要
--------------

*版本控制系统是软件项目协作开发必不可或缺的工具. 很多开源和闭源的项目都在积极准备, 或是已经把它们的源码库从集中式的版本控制系统 (CVCS) 迁移到分布式版本控制系统 (DVCS). 本文我们将总结 CVCS 和 DVCS 的区别, 并记述一些项目为了证明迁移的合理性, 提出的理论依据和预期收效.*


.. _intro:

引言
---------------------

对于很多项目而言, 它们的版本控制系统 (VCS), 以及其它工具如问题跟踪系统等, 是如何组织开发工作的核心. 管理软件开发的首要挑战是调整变更流程, 来协调大量地理位置上可能呈分布的软件开发人员, 且不以牺牲质量或带来过度开销为代价. 很大程度上, 这些工具决定了成员参与到项目是否方便, 如何协作开发新特性, 不同开发分支的合并频率, 如何进行代码评审以及如何组织对已经发布的代码进行后续支持. 撇开它们的重要性不谈, 这些工具对开发工作施加的影响和相关的取舍, 尚未被充分研究过.

新一代的 *分布式* VCS (DVCS), 开始崭露头角以解决当前的集中式 VCS (CVCS) , 如 CVS [1]_ [5]_ 和 Subversion [4]_ 等存在的一些局限, 并对分布式工作流提供更好的支持. 部分 DVCS, 如 GIT [I]_, MERCURIAL [II]_, BZR [III]_, 以及 BitKeeper [IV]_, 已经非常成熟, 很多开源和闭源项目计划或已经把他们的源码库迁移到了 DVCS.

作为一个围绕着版本控制进行实践探索和工具支持的大型研究项目的组成部分, 我们启动了一个定性研究以解答两个研究问题. 第一, 这些项目看到 DVCS 能够带来哪些好处? 将源码库切换到新的 VCS 需要付出巨大的投入 [V]_, 所以我们断定一定是有非常紧迫的原因, 以致非切换不可. 第二, 在切换的过程中, 这些项目对它们的开发过程做了哪些调整? 为了回答这两个问题, 我们仔细研究了 4 个已经或正在谋划迁移到 DVCS 的开源项目 (Perl, OpenOffice, NetBSD, Python) 相关公开文档和邮件列表讨论, 以便能够发现它们为了说服迁移提出的理论依据和潜在好处. 本文我们将从我们仍在进行中的分析报告中, 摘取一些初步观察的资料.

本文按如下形式组织. 在第二节, 我们提供一些背景资料, 汇总 VCS 的使用情况和 DVCS 区别于 CVCS 的简短说明. 在第三节, 我们总结预期的收效, 和部分已经或考虑迁移的开源项目很可能会报告的问题. 我们最后在第四节做出结论.


.. [I] git-scm.com; retrieved 2009/01/20
.. [II] www.selenic.com/mercurial/; retrieved 2009/01/20
.. [III] bazaar-vcs.org; retrieved 2009/01/20
.. [IV] bitkeeper.com; retrieved 2009/01/20
.. [V] For example, Perl 基金会的报告说他们迁移到 GIT 花了将近 21 months, 并导致大量的手工操作 [9]_.


.. _background:


背景资料
-----------------

本节我们对集中式和分布式 VCS 分别做一个简要描述, 并着重笔墨在被研究的开源项目. 注意, 由于各种 DVCS 的实现仍然在不断的快速发展中, 对当前工具的特性一一进行详细对比无疑会很快过时. 所以我们只对比 CVCS 和 DVCS 之间概念上的区别, 感兴趣的读者可以参考 Raymond 的 VCS 详细对比调查草案 [8]_.


集中式 VCS
~~~~~~~~~~~~~~~~~~

目前使用最为广泛版本控制系统 (VCS) 是集中式 VCS, 典型代表是 CVS [1]_ [5]_ 和 Subversion [4]_. 这些 VCS 之所以是集中式的, 是因为它们具有单一的权威源码库. 所有开发人员通过 *签出* (checkout) 动作获取该库源文件进行工作, 实质上是源码库某个时刻的快照.

源码库的写权限通常限制在部分开发者, 或 *提交者*. 在开源环境下, 提交者通常通过提交能证明其高水准编程能力的高质量补丁和遵守项目开发的约定, 来获得和保留写权限. 开发团队通常会确立代码约定和实践准则来管理提交到源码库的改动, 以保证源码的质量.

最新的 VCS 通常使用 *分支* (branches) 来支持源码库内代码的并行演化. 有个广为普及的实践准则: 维护一个 *主干* 分支作为当前的开发投入, 并从主干拉出新的分支作为产品已发布的版本, 并用于跟踪已发布产品的缺陷修复 [11]_. 分支也常常在很长一段时间内承担大量代码变更, 目的是将变更合并回主干分支.


分布式 VCS
~~~~~~~~~~~~~~~~~~~~~~~~~~

DVCS 不像 CVCS 那样要求一个中央主库. 对于 DVCS 而言, 每次签出的本身就是一个功能完整的库, 包含全部提交历史的副本. 写操作不再是问题, 因为每个开发者都可以毫无顾忌的对他们私有的库提交代码, 不用理会他们是不是被项目认可的提交者.

因为每个 DVCS 库都是一个完整的库, 所以不强制建立主干分支. 相反, 权威分支通过开发团队或社区之间的约定来确定, 有些项目甚至可能拥有多个主要分支. 比如, Linux 内核的官方分支是 Linus Torvalds 的分支 [6]_, 但也还有其它几个重要分支, 比如 Andrew Morton 的 ``-mm`` 分支, 用来演示和评估计划进行的内核改动. 一旦这些非稳态分支的补丁变得稳定, 并有其价值, Torvalds 便把补丁合并到他的主分支.

由于 DVCS 库包含所有修订历史, 使得它们很适合分布式和离线开发. 实际上, 这也是第一个有记载的 DVCS 最初开发动因, Reliable Software’s Code Co-op, 发行于 1997 [7]_. 打造可靠软件需要考虑地域分散的团队情况, 访问中央库的延时带来的代价是高昂的 [7]_. 使用 DVCS 很自然的使源码库可被随处复制, 一个副效益是降低灾难事件发生的风险.


项目
~~~~~~~~~~~~

以下 4 个开源项目的公开文档和邮件列表我们还尚在分析过程中.

Perl:
    Perl 基金会最近完成了把他们的代码库切换到 GIT 的工作. Perl 源码以前一直使用 Perforce VCS 维护, 由 ActiveState 公司托管, 该公司为 Perl 提交者提供免费的 Perforce 许可. 我们从多个着重讨论迁移计划的 wiki 页面, 和多个归档的邮件列表讨论话题收集数据. 尽管如此, 我们还不是很清楚切换到 GIT 的决定是如何做出的.

OpenOffice:
    OpenOffice 是一个由 Sun Microsystems 协调的大型开源项目. OpenOffice 源码以前用 CVS 维护, 他们对迁移到新的 VCS 做过积极的计划, 以解决长期使用 CVS 堆积的问题. 但由于 "[OpenOffice CVS 库] 在 OOo 长达 8 年开发成果的重压之下已经摇摇欲坠", 项目过早被迫迁移到 Subversion, 这是他们开发过程中大量使用分支, 导致分支数目一度达到 3000 产生的副作用. 在 CVS 中拉分支和打标签代价很高, 而且都不是原子操作, 需要在库的每个文件插入对分支或标签的引用. OOo 项目计划在 2009 年重新评估和选择 VCS. 我们数据来自多个归档的邮件列表讨论主题, 和描述当前开发过程, 对候选 VCS 使用经验的评价, 以及记录迁移计划等多处 wiki 页面.

Python:
    Python Software 基金会正在考虑把他们的代码库从 Subversion 切换到 DVCS. 我们得到的有关 Python 团队做出决定的过程来自一份扩展文档, 一个 Python 优化请求 (PEP), 以及多个归档的邮件列表讨论主题. PEP (译注: 指 `PEP 374`_) 是基金会制定决策的核心程序, 主要考察不同工具在一系列项目相关的 "使用环境" 下提供多大力度的支持. 使用环境和工具在开发团队的邮件列表中已有过讨论. 不过一切都尚未有定论, PEP 目前也在持续开发当中 [2]_. (译注: 截止到 2009-05-16, `PEP 374`_ 已经接近完成, Guido 也已宣布将迁移到 Mercurial_).

NetBSD:
    NetBSD 项目早在 1993 年, 项目启动初期就使用 CVS 库维护它的源代码. 一些 NetBSD 开发人员建议, 鉴于不断有开源项目从 CVS 迁出, NetBSD 也是时候考虑一下使用新的 VCS 了. 迁移还可能有机会摆脱 CVS 带来的困扰, 尤其是 CVS 中分支维护相关的众多问题. 邮件列表中, 对可能的迁移方案的讨论仍在继续. NetBSD 项目非常重视迁移是否能保留项目的所有修订历史.


调查结果
----------------

期望的收效
~~~~~~~~~~~~~~~~~~

方便所有开发人员的访问:
    大多数项目向 DVCS 迁移的关键原因之一是: 对非提交者更友好. 没有提交权限的贡献者在开发时很难从 CVCS 中受益, 常常需要采用创建并行库的方式来管理较大的代码变更. 在 Python 的讨论中, 这个问题被特别强调, 因为 CVCS 最大的局限就是 "任何为 Python 写补丁或对其进行定制的开发人员, 版本修订时得不到工具的直接支持". Perl 基金会强调 DVCS 必须是开源的, 以确保社区所有成员都可以使用该工具. OpenOffice 开发过程主要依赖 CVS 分支, 开发人员必须要有该库的写权限.
    
    在 DVCS 中, 每个贡献者有他们自己的库, 而且他们能够 "随时保存他们的工作进度, 让开发过程更轻松". Torvalds (GIT 之父) 认为分布式系统的特性避免了项目围绕着获取 (和回收) 向中央库提交代码权限的政治纷争 [10]_ (译注: 关于 Torvalds 政治纷争的观点详细解释可 `进一步阅读 <http://people.debian.org.tw/~chihchun/2008/12/19/linus-torvalds-on-git/>`_). 当贡献者正在进行重大修改, 或评审过程需要贡献者反复修改提交的代码时, 这个特点显得尤为重要.

支持原子变更:
    NetBSD 和 OpenOffice 项目最紧迫的需求是要求新的 VCS 支持源码库范围的原子提交. 两个团队都遭遇过使用 CVS 分支导致库朽化, 而且这个问题可能难以修复.

简单的自动合并:
    DVCS 保存了充足的信息来支持自动和反复合并, 长期维护的分支之间常常会进行这类合并. Python 项目认为这是一个重要特性, 主要出于两个原因. 一, 改进对合并的支持可以鼓励开发人员保持他们的分支和主干开发同步, 并降低他们的分支趋向陈旧过期的风险. 二, 改进对合并的支持减少提交者的负担, Perl 项目也认为这点很重要. 交换简单的补丁文件会有版本不匹配的风险,  补丁作者使用的版本和补丁评审者的版本很可能不一致. DVCS 生成的补丁文件包含充分的依赖信息, 以甄别补丁是否依赖其它没有提交的修订版本, 由此减少判断 "问题补丁" 的工作量. 同时依赖信息能有效的鉴别共同祖先, 有利于改进补丁的合并工作.

改进对 "试验田" 的支持:
    Perl 和 OpenOffcie 项目试图加强对非提交者的支持, 让他们在提交修改进行合并之前能够自主的进行试验. 低成本的分支让开发人可以进行本地提交, 跟踪和记录开发进度, 这种方式通常很适合着手一些对结果不确定的尝试性工作.

支持离线操作:
    Python 项目格外希望支持离线操作, 一个在开发者乘飞机旅行时非常有用的特性. CVCS 工具要求开发人员必须连上服务器才能对源码库进行访问和查询. 这种离线的特性把提交修改 (如新建快照) 从公布修改 (译注: 指提交到中央库, 让其他人也能看到修改) 中分离出来 [3]_.


迁移和挑战
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Perl 团队在邮件列表中也探讨过迁移到新 VCS 所需的工作. 比如, 其中一个贡献者开玩笑的说道, 如果他们不能及时调整开发教程文档以适应新的工作流, 可能导致 "所有的提交都将停止". 迁移的工作量是可观的, 因此我们认为迁移的理由也应该非常充分.

确保迁移能够顺利进行的挑战之一是改变团队的开发过程. 一些团队在这方面比其它团队更为开放. 举个例子, 在评估不同的 VCS 时, OpenOffice 团队倾向于优先考虑能够满足当前 (大规模) 开发过程的工具. Python 团队则详尽的记录一旦开始迁移, 他们期望的新的开发方式应该是什么样的. 我们很有兴趣了解在新的 VCS 影响下, 开发过程将产生哪些变化.

NetBSD 和 Perl 开发者关心他们的元数据如何从以前的 VCS 迁移到新的 VCS. 元数据 (如文件版本号) 被嵌入在提交记录和其它文档中, 并被到处引用. 在转换到 GIT 的过程中, Perl 在每次提交记录中插入一个特殊的信息头, 它包含对应的 Perforce 版本号 (``p4raw-id:NNNN`` 的格式). 另外还需要额外处理代码作者的相关属性, 类似 **ohloh.net** 等网站用它来统计开发人员的一些指标.

有的 NetBSD 开发人员尤其偏爱直观的提交标识符 (如, 单步递增的版本号), 部分 DVCS 使用 SHA1 形式的提交标识符不合他们的意. 用来通知相关人员的邮件常常会使用这些标识符 (特别是缺陷修复) . 这个问题可以通过对特定修订版本进行打标签的方式来绕过去. 但是打标签的方式不一定适用所有情况. DVCS 中, 一个标签只对那些从打过标签的库更新过的库可见; 所以一个标签想要可靠的在全局范围代替一个特定修订版本的话, 它必须被权威库接纳. 但滥打标签同样可能会对已有的标签空间造成污染, 虽然还不清楚滥用到何种程度才算是问题.

每个 DVCS 库都是一个完整的副本会引起一些副作用. 1992 年, UNIX System Laboratories 对抗 Regents of the University of California and Berkeley Software Design Inc. 的一系列法律诉讼最终裁定某些源代码文件必须从 NetBSD 源码库删除 [6]_. 如果使用 DVCS 的话, 根本不可能履行裁定: 一旦变更发布到公开库, 该变更可能会被复制到其它很多地方.

最后, 大多数开发人员需要对源码库管理方式做出重大调整来适应 DVCS. 各个项目也都要面对巨大的挑战 - 向它们的开发者宣传迁移的理论依据, 以及编写教程和迁移文档来降低学习曲线.


总结及后续工作
-----------------------

DVCS 获得了大量的精神支持, 至少很多项目都在讨论把源码库迁移到 DVCS 的积极意义. 我们的研究对 CVCS 的局限, 和这些局限给开发团队带来的负面影响提供了一些见解. 虽然 DVCS 解决了 CVCS 的一些问题, 尤其是分支反复合并的难题, 我们的研究结果是 DVCS 可能也会引入新的问题.

到目前为止, 我们只探究了团队成员 *相信* 迁移到 DVCS 所将带来的影响. 这些信念帮助形成若干假定 (如, 使用 DVCS 将使非提交者对项目做出更大贡献), 我们将对此做更进一步的探究. 我们的研究下一步将对同时拥有 DVCS 和 CVCS 经验的开发者进行调查. 我们很有可能以提问的方式, 比如: 迁移到 DVCS 真的减少了分享的障碍吗? DVCS 迫使他们的开发过程做了哪些调整? 使用 DVCS 带来了哪些新的问题? 他们会向其它正在考虑迁移到 DVCS 的项目提供什么建议? 在什么环境下他们会建议不要迁移? DVCS 在开源和闭源项目中的使用有区别吗?

参考资料
----------------------

.. [1] B.Berliner. CVS II: Parallelizing software development. In Proc. USENIX Winter 1990 Technical Conference, pages 341–352, Berkeley, USA, 1990. USENIX Association.

.. [2] B.Cannon, B.Warsaw, S.J.Turnbull, and A.Vassalotti. Migrating from Subversion to a distributed VCS. PEP 0374, Python Foundation, draft. URL http://www.python.org/dev/peps/pep-0374/. Retrieved 2009/01/16.

.. [3] I.C.Clatworthy. Distributed version control: Why and how. In Proc. Open Source Development Conf. (OSDC), 2007.

.. [4] B.Collins-Sussman, B.W.Fitzpatrick, and C.M.Pilato. Version Control with Subversion (for Subversion 1.5). O’Reilly, 2 edition, 2008.

.. [5] D.Grune. Concurrent Versions Systems: A method for independent cooperation. Technical Report IR 113, Vrije Universiteit, 1986.

.. [6] P.Jones. The 1994 USL–Regents of UCal settlement agreement. Groklaw, Nov. 2004. URL http://www.groklaw.net/articlebasic.php?story=20041126130302760.

.. [7] B.Milewski. Distributed source control system. In Proc. ICSE Worksh. on System Configuration Management (SCM-7), pages 98–107, 1997.

.. [8] E.S.Raymond. Understanding version-control systems. Retrieved 2009/01/17 from http://www.catb.org/~esr/writings/version-control/, draft.

.. [9] The Perl Foundation. Perl 5 now uses git for version control, Dec. 2008. URL http://use.perl.org/articles/08/12/22/0830205.shtml.

.. [10] L.Torvalds. Linus torvalds on git. Transcript from Google Tech Talk, May 2007. URL http://git.or.cz/gitwiki/LinusTalk200705Transcript.

.. [11] L.Wingerd and C.Seiwald. High-level SCM best practices. In System Configuration Management, volume 1439 of LNCS, pages 57–66. Springer, 1998.


.. _PEP 374: http://www.python.org/dev/peps/pep-0374/
.. _Mercurial: http://www.selenic.com/mercurial/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
