import mock

from qidoc.test.conftest import TestDocWorkTree
from qidoc.builder import DocBuilder

def test_doc_builder_solve_deps_by_default():
    doc_worktree = mock.Mock()
    deps_solver = mock.Mock()
    general_doc = mock.Mock()
    qibuild_doc = mock.Mock()
    deps_solver.return_value = [general_doc, qibuild_doc]

    doc_builder = DocBuilder(doc_worktree)
    doc_builder.base_project = [general_doc]
    doc_builder.deps_solver = deps_solver
    doc_builder.configure()
    assert general_doc.configure.called
    assert qibuild_doc.configure.called

def test_using_dash_s():
    doc_worktree = mock.Mock()
    deps_solver = mock.Mock()
    general_doc = mock.Mock()
    qibuild_doc = mock.Mock()
    deps_solver.return_value = [general_doc, qibuild_doc]

    doc_builder = DocBuilder(doc_worktree)
    doc_builder.single = True
    doc_builder.base_project = [general_doc]
    doc_builder.deps_solver = deps_solver
    doc_builder.configure()
    doc_builder.build()
    assert general_doc.build.called
    # always configure the deps
    assert qibuild_doc.configure.called
    # but don't build them
    assert qibuild_doc.build.called
